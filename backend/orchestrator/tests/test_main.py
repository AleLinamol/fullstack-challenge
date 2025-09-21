from fastapi.testclient import TestClient
from app.main import app
from app.jsonrpc_client import JSONRPCError

client = TestClient(app)

def test_chat_valid_message(monkeypatch):
    mock_result = {"id": 7, "name": "Usuario 7"}

    async def mock_call_agent(intent):
        return mock_result

    monkeypatch.setattr("app.main.call_agent", mock_call_agent)

    response = client.post("/chat", json={"message": "usuario 7"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert data["result"] == mock_result
    assert data.get("error") is None

def test_chat_unknown_intent():
    response = client.post("/chat", json={"message": "mensaje desconocido"})
    assert response.status_code == 200
    data = response.json()
    assert data.get("error") == "Intención no reconocida."
    assert "examples" in data

def test_chat_validation_error():
    response = client.post("/chat", json={})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    assert data.get("message") == "Error de validación en la entrada."

def test_chat_jsonrpc_error(monkeypatch):
    async def mock_call_agent(intent):
        raise JSONRPCError(-32000, "Error simulado JSON-RPC")

    monkeypatch.setattr("app.main.call_agent", mock_call_agent)

    response = client.post("/chat", json={"message": "usuario 7"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Error simulado JSON-RPC" in data["detail"]

def test_chat_empty_message():
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 200
    data = response.json()
    assert data.get("error") == "Intención no reconocida."

def test_chat_special_characters(monkeypatch):
    mock_result = {"results": []}

    async def mock_call_agent(intent):
        return mock_result

    monkeypatch.setattr("app.main.call_agent", mock_call_agent)

    response = client.post("/chat", json={"message": "!@#$%^&*()"})
    assert response.status_code == 200
    data = response.json()
    assert "error" in data or "result" in data

def test_chat_response_content_type(monkeypatch):
    mock_result = {"id": 1}

    async def mock_call_agent(intent):
        return mock_result

    monkeypatch.setattr("app.main.call_agent", mock_call_agent)

    response = client.post("/chat", json={"message": "usuario 1"})
    assert response.headers["content-type"] == "application/json"
