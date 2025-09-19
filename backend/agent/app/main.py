from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI()
AGENT_KEY = "challenge-token-123"

@app.post("/rpc")
async def rpc_endpoint(request: Request, x_agent_key: str = Header(None)):
    if x_agent_key != AGENT_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = await request.json()
    except Exception:
        return {"error": "JSON inválido"}

    if not isinstance(payload, dict) or "jsonrpc" not in payload or "method" not in payload or "id" not in payload:
        return {"error": "JSON-RPC inválido"}

    return {"message": "JSON válido", "method": payload["method"]}
