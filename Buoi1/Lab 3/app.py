from __future__ import annotations

from flask import Flask, jsonify, request

from securelogger import SecureLogger
from securevalidator import (
    sanitize_html_input,
    sanitize_sql_input,
    validate_email,
    validate_filename,
    validate_url,
)

app = Flask(__name__)
logger = SecureLogger()

VALIDATORS = {
    "email": validate_email,
    "url": validate_url,
    "filename": validate_filename,
    "sql": sanitize_sql_input,
    "html": sanitize_html_input,
}


@app.get("/")
def index():
    return jsonify({
        "lab": "Buoi1 - Lab 3 - SecureLogger",
        "endpoints": {
            "POST /validate": {"validator": "email|url|filename|sql|html", "value": "input"},
            "POST /log": {"level": "DEBUG|INFO|WARNING|ERROR|CRITICAL", "message": "text"},
            "GET /logs/integrity": "kiem tra log co bi thay doi khong",
        },
    })


@app.post("/validate")
def validate():
    data = request.get_json(silent=True) or {}
    validator_name = data.get("validator")
    value = data.get("value", "")

    if validator_name not in VALIDATORS:
        logger.warning("invalid_validator_requested", validator=validator_name, input=value)
        return jsonify({"error": "validator không hợp lệ"}), 400

    result = VALIDATORS[validator_name](value)
    logger.log_validation(validator_name, value, result)
    return jsonify({"validator": validator_name, "input": value, "result": result})


@app.post("/log")
def write_log():
    data = request.get_json(silent=True) or {}
    level = data.get("level", "INFO")
    message = data.get("message", "")
    context = data.get("context", {})
    logger.log(level, message, **context)
    return jsonify({"logged": True, "level": level.upper()})


@app.get("/logs/integrity")
def logs_integrity():
    return jsonify({"integrity_ok": logger.verify_integrity()})


if __name__ == "__main__":
    app.run(debug=True)
