import json
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pathlib import Path
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()  
AGENT_KEY = os.getenv("AGENT_KEY")


# Cargar datos de seed.json al iniciar la app
DATA_FILE = Path(__file__).parent / "seed.json"
try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
except Exception as e:
    users = []
    print(f"Error cargando seed.json: {e}")

def jsonrpc_error(code, message, req_id=None):
    return JSONResponse(
        status_code=200,
        content={
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    )

def get_user(params):
    user_id = params.get("id")
    if user_id is None:
        raise ValueError("Falta parámetro 'id'")
    for user in users:
        if user.get("id") == user_id:
            return user
    raise ValueError(f"Usuario con id {user_id} no encontrado")

def search_users(params):
    query = params.get("query", "").lower()
    if not query:
        return users  # Si no hay query, devuelve todos
    return [u for u in users if query in u.get("name", "").lower()]

def list_users(params):
    # Ignora params, devuelve todos los usuarios
    return users

@app.post("/rpc")
async def rpc_endpoint(request: Request, x_agent_key: str = Header(None)):
    if x_agent_key != AGENT_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        payload = await request.json()
    except Exception:
        return jsonrpc_error(-32700, "Parse error")

    if not isinstance(payload, dict):
        return jsonrpc_error(-32600, "Invalid Request")

    jsonrpc = payload.get("jsonrpc")
    method = payload.get("method")
    req_id = payload.get("id")
    params = payload.get("params", {})

    if jsonrpc != "2.0" or not method or req_id is None:
        return jsonrpc_error(-32600, "Invalid Request", req_id)

    try:
        if method == "get_user":
            result = get_user(params)
        elif method == "search_users":
            result = search_users(params)
        elif method == "list_users":
            result = list_users(params)
        else:
            return jsonrpc_error(-32601, "Method not found", req_id)
    except Exception as e:
        return jsonrpc_error(-32602, str(e), req_id)

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": result
    }
 