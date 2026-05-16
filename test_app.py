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
