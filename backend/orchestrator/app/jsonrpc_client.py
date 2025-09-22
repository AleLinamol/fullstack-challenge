import httpx
import uuid
import asyncio
from app.config import AGENT_URL, AGENT_KEY, HTTP_TIMEOUT, MAX_RETRIES
from app.errors import JSONRPCError

async def call_agent(intent: dict) -> dict:
    if not AGENT_KEY:
        raise JSONRPCError(-32000, "Missing or invalid X-Agent-Key")

    method = intent["kind"]
    params = {}

    if method == "get_user":
        if "id" not in intent:
            raise ValueError("El parámetro 'id' es requerido para get_user")
        params = {"id": intent["id"]}
    elif method == "search_users":
        if "query" not in intent:
            raise ValueError("El parámetro 'query' es requerido para search_users")
        params = {"query": intent["query"]}
    elif method == "list_users":
        if "limit" not in intent:
            raise ValueError("El parámetro 'limit' es requerido para list_users")
        params = {"limit": intent["limit"]}
    else:
        raise ValueError("Intento de llamar método desconocido")

    request_id = str(uuid.uuid4())
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params
    }

    headers = {
        "Content-Type": "application/json",
        "X-Agent-Key": AGENT_KEY
    }

    last_exc = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                response = await client.post(AGENT_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
            break
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            last_exc = e
            if attempt == MAX_RETRIES:
                raise JSONRPCError(-32001, f"Error contacting Agent: {str(e)}")
            await asyncio.sleep(0.5 * attempt)  
    else:
        raise JSONRPCError(-32001, "Max retries exceeded contacting Agent")

    if "error" in data:
        err = data["error"]
        raise JSONRPCError(err.get("code", -32000), err.get("message", "Unknown error"))

    if "result" not in data:
        raise JSONRPCError(-32603, "Invalid response: missing result")

    return data["result"]
