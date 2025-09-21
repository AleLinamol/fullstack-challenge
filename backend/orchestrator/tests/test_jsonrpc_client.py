import pytest
import respx
from httpx import Response
from app.jsonrpc_client import call_agent, JSONRPCError

@pytest.fixture
def patch_agent_url(monkeypatch):
    monkeypatch.setattr("app.jsonrpc_client.AGENT_URL", "http://agent.test/jsonrpc")

@respx.mock
@pytest.mark.asyncio
async def test_call_agent_success(patch_agent_url):
    respx.post("http://agent.test/jsonrpc").mock(
        return_value=Response(200, json={
            "jsonrpc": "2.0",
            "id": "123",
            "result": {"id": 7, "name": "Usuario 7"}
        })
    )

    intent = {"kind": "get_user", "id": 7}
    result = await call_agent(intent)
    assert result["id"] == 7

@respx.mock
@pytest.mark.asyncio
async def test_call_agent_error_response(patch_agent_url):
    respx.post("http://agent.test/jsonrpc").mock(
        return_value=Response(200, json={
            "jsonrpc": "2.0",
            "id": "123",
            "error": {"code": -32601, "message": "Method not found"}
        })
    )

    intent = {"kind": "get_user", "id": 7}
    with pytest.raises(JSONRPCError) as excinfo:
        await call_agent(intent)
    assert "Method not found" in str(excinfo.value)
