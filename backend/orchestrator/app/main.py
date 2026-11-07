import logging
import httpx
from app.config import AGENT_URL
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from app.intent_parser import parse_intent
from app.jsonrpc_client import call_agent, JSONRPCError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orchestrator")

class ChatRequest(BaseModel):
    message: str = Field(..., example="usuario 2")

class ChatResponse(BaseModel):
    result: dict | list | None = None
    error: str | None = None
    examples: list[str] | None = None

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body, "message": "Error de validación en la entrada."},
    )

@app.exception_handler(JSONRPCError)
async def jsonrpc_exception_handler(request: Request, exc: JSONRPCError):
    logger.error(f"JSONRPCError: {exc}")
    if exc.code == -32001:
        return JSONResponse(status_code=503, content={"error": "Agent temporalmente no disponible"})
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"},
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    logger.info(f"Received message: {req.message}")
    intent = parse_intent(req.message)
    if intent["kind"] == "unknown":
        logger.warning(f"Unknown intent for message: {req.message}")
        return ChatResponse(
            error="Intención no reconocida.",
            examples=[
                "usuario 2",
                "buscar ana",
                "lista 3"
            ]
        )
    result = await call_agent(intent)
    logger.info(f"Agent result: {result}")
    return ChatResponse(result=result)


@app.get("/health")
async def health():
    try:
        if not AGENT_URL:
            raise ValueError("Agent URL not configured")
        url = str(httpx.URL(AGENT_URL).copy_with(path="/health"))
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(url)
            response.raise_for_status()
        return {"status": "ok"}
    except (httpx.HTTPError, ValueError):
        return JSONResponse(status_code=503, content={"status": "starting"})
