from fastapi.testclient import TestClient
from app.main import app

def test_agent_rejects_unconfigured_key(monkeypatch):
    monkeypatch.setattr("app.main.AGENT_KEY", None)
    assert TestClient(app).post("/rpc", json={}).status_code == 401

def test_agent_requires_correct_key(monkeypatch):
    monkeypatch.setattr("app.main.AGENT_KEY", "test-secret")
    client = TestClient(app)
    assert client.post("/rpc", headers={"X-Agent-Key": "wrong"}, json={}).status_code == 401
    response = client.post("/rpc", headers={"X-Agent-Key": "test-secret"}, json={"jsonrpc": "2.0", "id": 1, "method": "get_user", "params": {"id": 2}})
    assert response.json()["result"][0]["id"] == 2
