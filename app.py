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
