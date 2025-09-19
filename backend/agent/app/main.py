from fastapi import FastAPI, Header, HTTPException

app = FastAPI()
AGENT_KEY = "challenge-token-123"

@app.post("/rpc")
async def rpc_endpoint(x_agent_key: str = Header(None)):
    if x_agent_key != AGENT_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"message": "Clave válida"}
