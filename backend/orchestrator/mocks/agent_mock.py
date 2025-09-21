from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()

# Datos semilla
USERS = [
    {"id": 1, "name": "Ana López", "email": "ana@elogia.tech", "role": "admin", "createdAt": "2025-05-01T10:00:00Z"},
    {"id": 2, "name": "Bruno Díaz", "email": "bruno@elogia.tech", "role": "viewer", "createdAt": "2025-06-10T15:30:00Z"},
    {"id": 3, "name": "Carla Ríos", "email": "carla@elogia.tech", "role": "editor", "createdAt": "2025-07-21T09:12:00Z"},
]

load_dotenv() 

AGENT_KEY = os.getenv("AGENT_KEY")

class JSONRPCRequest(BaseModel):
    jsonrpc: str
    id: str
    method: str
    params: dict = {}

@app.post("/rpc")
async def rpc_endpoint(request: Request):
    # Validar header X-Agent-Key
    agent_key = request.headers.get("X-Agent-Key")
    if agent_key != AGENT_KEY:
        return JSONResponse(
            status_code=401,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32000, "message": "Unauthorized: Invalid or missing X-Agent-Key"}
            }
        )

    body = await request.json()
    try:
        req = JSONRPCRequest(**body)
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"}
            }
        )

    # Manejar métodos
    if req.method == "get_user":
        user_id = req.params.get("id")
        user = next((u for u in USERS if u["id"] == user_id), None)
        if user:
            return {"jsonrpc": "2.0", "id": req.id, "result": user}
        else:
            return {"jsonrpc": "2.0", "id": req.id, "error": {"code": -32001, "message": "User  not found"}}

    elif req.method == "search_users":
        query = req.params.get("query", "").lower()
        limit = req.params.get("limit", 5)
        results = [u for u in USERS if query in u["name"].lower() or query in u["email"].lower()]
        return {"jsonrpc": "2.0", "id": req.id, "result": results[:limit]}

    elif req.method == "list_users":
        limit = req.params.get("limit", 5)
        return {"jsonrpc": "2.0", "id": req.id, "result": USERS[:limit]}

    else:
        return {"jsonrpc": "2.0", "id": req.id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
