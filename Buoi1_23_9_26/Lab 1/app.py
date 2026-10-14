from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from securevalidator import (
    sanitize_html_input,
    sanitize_sql_input,
    validate_email,
    validate_filename,
    validate_url,
)

app = Flask(__name__)

VALIDATORS = {
    "email": validate_email,
    "url": validate_url,
    "filename": validate_filename,
    "sql": sanitize_sql_input,
    "html": sanitize_html_input,
}


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/validate")
def validate():
    data = request.get_json(silent=True) or request.form
    validator_name = data.get("validator")
    value = data.get("value", "")

    if validator_name not in VALIDATORS:
        return jsonify({"error": "validator không hợp lệ"}), 400

    result = VALIDATORS[validator_name](value)
    return jsonify({"validator": validator_name, "input": value, "result": result})


if __name__ == "__main__":
    app.run(debug=True)
