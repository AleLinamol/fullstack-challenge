from fastapi import FastAPI
from pydantic import BaseModel
from app.intent_parser import parse_intent

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
    # Simula respuesta exitosa con la intención detectada
    return {
        "intent": intent,
        "message": f"Intención detectada: {intent['kind']}"
    }
