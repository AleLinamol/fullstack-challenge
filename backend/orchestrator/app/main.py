from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.intent_parser import parse_intent
from app.jsonrpc_client import call_agent, JSONRPCError

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    intent = parse_intent(req.message)
    if intent["kind"] == "unknown":
        return {
            "error": "Intención no reconocida.",
            "examples": [
                "usuario 7",
                "buscar ana",
                "lista 3"
            ]
        }
    try:
        result = await call_agent(intent)
        return {"result": result}
    except JSONRPCError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
