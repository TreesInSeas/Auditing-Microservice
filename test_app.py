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
