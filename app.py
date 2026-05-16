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
    """Return True if the email has a basic valid email format."""
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
