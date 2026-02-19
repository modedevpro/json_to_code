# Developer: محمود عادل الغريب
# JSON → Python / PHP Code Generator
# Safe for Vercel

from flask import Flask, request, Response
import json
import requests

app = Flask(__name__)

def safe_py_to_python(value, indent=0):
    sp = "    " * indent
    if isinstance(value, list):
        items = [safe_py_to_python(v, indent + 1) for v in value]
        return "[\n" + sp + "    " + (",\n" + sp + "    ").join(items) + "\n" + sp + "]"
    if isinstance(value, dict):
        items = [f"'{k}': {safe_py_to_python(v, indent + 1)}" for k, v in value.items()]
        return "{\n" + sp + "    " + (",\n" + sp + "    ").join(items) + "\n" + sp + "}"
    if isinstance(value, bool): return "True" if value else "False"
    if value is None: return "None"
    if isinstance(value, (int,float)): return str(value)
    s = str(value)
    return "'" + s.replace("'", "\\'") + "'"

def safe_py_to_php(value, indent=0):
    sp = "    " * indent
    if isinstance(value, list):
        items = [safe_py_to_php(v, indent + 1) for v in value]
        return "[\n" + sp + "    " + (",\n" + sp + "    ").join(items) + "\n" + sp + "]"
    if isinstance(value, dict):
        items = [f"'{k}' => {safe_py_to_php(v, indent + 1)}" for k,v in value.items()]
        return "[\n" + sp + "    " + (",\n" + sp + "    ").join(items) + "\n" + sp + "]"
    if isinstance(value, bool): return "true" if value else "false"
    if value is None: return "null"
    if isinstance(value,(int,float)): return str(value)
    s = str(value)
    return "'" + s.replace("'", "\\'") + "'"

@app.route("/", methods=["GET","POST"])
def generate():
    try:
        lang = request.args.get("lang")
        json_data = request.form.get("data")
        url = request.args.get("url")

        # fetch URL safely
        if url:
            try:
                r = requests.get(url, timeout=3)
                json_data = r.text
            except:
                return Response("ERROR: Failed to fetch URL\n", mimetype="text/plain")

        if not json_data:
            return Response("ERROR: No JSON provided\n", mimetype="text/plain")

        try:
            data = json.loads(json_data)
        except Exception as e:
            return Response(f"ERROR: Invalid JSON\n{str(e)}", mimetype="text/plain")

        # generate output safely
        output = ""
        if lang == "python":
            output += "# Auto-generated Python file\n\n"
            output += "data = " + safe_py_to_python(data) + "\n\n"
            output += "# Print all values\n"
            output += "print(data)"
        elif lang == "php":
            output += "<?php\n// Auto-generated PHP file\n\n"
            output += "$data = " + safe_py_to_php(data) + ";\n"
            output += "print_r($data);"
        else:
            return Response("ERROR: lang must be 'python' or 'php'\n", mimetype="text/plain")

        return Response(output, mimetype="text/plain")

    except Exception as e:
        return Response(f"CRASH:\n{str(e)}", mimetype="text/plain")
