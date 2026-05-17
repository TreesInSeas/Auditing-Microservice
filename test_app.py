import json
import pytest
import app as audit_app

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_log_file = tmp_path / "test_audit_log.json"
    monkeypatch.setattr(audit_app, "LOG_FILE", test_log_file)
    audit_app.app.config["TESTING"] = True
    with audit_app.app.test_client() as client:
        yield client
def test_add_valid_audit_log(client):
    response = client.post("/audit", json={
        "email": "user@example.com",
        "text": "Created an account"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["log"]["email"] == "user@example.com"
    assert data["log"]["text"] == "Created an account"
    assert "timestamp" in data["log"]
def test_reject_invalid_email(client):
    response = client.post("/audit", json={
        "email": "not-an-email",
        "text": "Created an account"
    })

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_reject_empty_text(client):
    response = client.post("/audit", json={
        "email": "user@example.com",
        "text": ""
    })

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_reject_text_over_1000_characters(client):
    response = client.post("/audit", json={
        "email": "user@example.com",
        "text": "x" * 1001
    })

    assert response.status_code == 400
    assert response.get_json()["success"] is False


def test_get_all_audit_logs(client):
    client.post("/audit", json={"email": "a@example.com", "text": "First event"})
    client.post("/audit", json={"email": "b@example.com", "text": "Second event"})

    response = client.get("/audit")

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["count"] == 2
