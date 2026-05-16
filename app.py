from flask import Flask, request, jsonify
from datetime import datetime, timezone
from pathlib import Path
import json
import re
import uuid

app = Flask(__name__)

LOG_FILE = Path("audit_log.json")
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
MAX_TEXT_LENGTH = 1000

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    return EMAIL_PATTERN.match(email.strip()) is not None

def load_logs() -> list:
    """Load audit logs from the JSON file."""
    if not LOG_FILE.exists():
        return []

    try:
        with LOG_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []
def save_logs(logs: list) -> None:
    """Save audit logs to the JSON file."""
    with LOG_FILE.open("w", encoding="utf-8") as file:
        json.dump(logs, file, indent=2)

@app.route("/audit", methods=["POST"])
def add_to_audit_log():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON."
        }), 400

    email = data.get("email", "")
    text = data.get("text", "")

    if not is_valid_email(email):
        return jsonify({
            "success": False,
            "error": "Invalid email format."
        }), 400

    if not isinstance(text, str) or len(text.strip()) == 0:
        return jsonify({
            "success": False,
            "error": "Text must be a non-empty string."
        }), 400

    if len(text) > MAX_TEXT_LENGTH:
        return jsonify({
            "success": False,
            "error": "Text must be fewer than 1000 characters."
        }), 400

    logs = load_logs()

    new_log = {
        "id": str(uuid.uuid4()),
        "email": email.strip().lower(),
        "text": text.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    logs.append(new_log)
    save_logs(logs)

    return jsonify({
        "success": True,
        "message": "Audit log added successfully.",
        "log": new_log
    }), 201

@app.route("/audit", methods=["GET"])
def get_audit_log():
    email = request.args.get("email")
    logs = load_logs()

    if email:
        if not is_valid_email(email):
            return jsonify({
                "success": False,
                "error": "Invalid email format."
            }), 400

        email = email.strip().lower()
        logs = [log for log in logs if log.get("email") == email]

    return jsonify({
        "success": True,
        "count": len(logs),
        "logs": logs
    }), 200
@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        "success": True,
        "message": "Auditing microservice is running."
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1234, debug=True)
