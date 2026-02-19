# Developer: محمود عادل الغريب

from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def generate():
    try:
        lang = request.args.get("lang")
        json_data = request.form.get("data")

        if not json_data:
            return Response("ERROR: No JSON provided\n", mimetype="text/plain")

        try:
            data = json.loads(json_data)
        except Exception as e:
            return Response(f"ERROR: Invalid JSON\n{str(e)}", mimetype="text/plain")

        if lang == "python":
            return Response("Python mode working", mimetype="text/plain")

        elif lang == "php":
            return Response("PHP mode working", mimetype="text/plain")

        else:
            return Response("ERROR: lang must be python or php\n", mimetype="text/plain")

    except Exception as e:
        return Response(f"CRASH:\n{str(e)}", mimetype="text/plain")
