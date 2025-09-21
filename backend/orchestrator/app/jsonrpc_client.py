import httpx
import uuid
from app.config import AGENT_URL, AGENT_KEY
from app.errors import JSONRPCError

class JSONRPCError(Exception):
    def __init__(self, code, message):
        super().__init__(f"JSON-RPC Error {code}: {message}")
        self.code = code
        self.message = message
    

async def call_agent(intent: dict) -> dict:
    if not AGENT_KEY or AGENT_KEY.strip() == "":
        raise JSONRPCError(-32000, "Missing or invalid X-Agent-Key")
    
    method = intent["kind"]
    params = {}

    if method == "get_user":
        params = {"id": intent["id"]}
    elif method == "search_users":
        params = {"query": intent["query"], "limit": 5}  # límite fijo o configurable
    elif method == "list_users":
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

    async with httpx.AsyncClient() as client:
        response = await client.post(AGENT_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    if "error" in data:
        err = data["error"]
        raise JSONRPCError(err.get("code", -32000), err.get("message", "Unknown error"))

    if "result" not in data:
        raise JSONRPCError(-32603, "Invalid response: missing result")
    


    return data["result"]
