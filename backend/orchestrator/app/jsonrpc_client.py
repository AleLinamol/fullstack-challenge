import httpx
import uuid
from dotenv import load_dotenv
import os


load_dotenv() 

AGENT_KEY = os.getenv("AGENT_KEY")
AGENT_URL = os.getenv("AGENT_URL")

class JSONRPCError(Exception):
    def __init__(self, code, message):
        super().__init__(f"JSON-RPC Error {code}: {message}")
        self.code = code
        self.message = message

async def call_agent(intent: dict) -> dict:
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
