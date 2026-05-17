# Auditing-Microservice
Auditing for password manager
This microservice records audit events for a password manager application. It supports adding logs and retrieving logs through a REST API.

## Features

- Add an audit log with an email, event text, and timestamp
- Validate email format
- Reject empty text
- Reject text longer than 1000 characters
- Retrieve all audit logs
- Retrieve audit logs for one email address
- Store logs in a local JSON file

## Install

```bash
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python app.py
```

The service runs at:

```text
http://127.0.0.1:1234
```

## Endpoints

### POST /audit

Adds a new audit log.

Request body:

```json
{
  "email": "email@email.com",
  "text": "Created an account"
}
```

Success response:

```json
{
  "success": true,
  "message": "Audit log added successfully.",
  "log": {
    "id": "generated-id",
    "email": "email@email.com",
    "text": "Created an account",
    "timestamp": "2026-05-16T12:00:00+00:00"
  }
}
```

### GET /audit

Returns all audit logs.

```bash
curl http://127.0.0.1:1234/audit
```

### GET /audit?email=email@email.com

Returns only logs for the provided email.

```bash
curl "http://127.0.0.1:1234/audit?email=email@email.com"
```

## Test

```bash
pytest
```
