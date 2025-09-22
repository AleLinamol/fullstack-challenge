import logging
from fastapi import FastAPI, Request, Header
from fastapi.responses import JSONResponse
from app.config import AGENT_KEY
from app.errors import (
    PARSE_ERROR,
    INVALID_REQUEST,
    METHOD_NOT_FOUND,
    INVALID_PARAMS,
    jsonrpc_error_response,
)
from app.rpc_handlers import handle_get_user, handle_search_users, handle_list_users

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

METHODS = {
    "get_user": handle_get_user,
    "search_users": handle_search_users,
    "list_users": handle_list_users,
}

@app.post("/rpc")
async def rpc_endpoint(request: Request, x_agent_key: str = Header(None)):
    if x_agent_key != AGENT_KEY:
        logger.warning("Unauthorized access attempt with invalid X-Agent-Key header")
        return JSONResponse(
            status_code=401,
            content={"error": "Unauthorized: Invalid X-Agent-Key header"},
        )

    try:
        payload = await request.json()
        logger.info(f"Received request payload: {payload}")
    except Exception as e:
        logger.error(f"Failed to parse JSON payload: {e}")
        return JSONResponse(
            status_code=200,
            content=jsonrpc_error_response(None, PARSE_ERROR),
        )

    jsonrpc = payload.get("jsonrpc")
    method = payload.get("method")
    params = payload.get("params", {})
    id_ = payload.get("id")

    # Log info de la petición
    logger.info(f"Processing RPC request id={id_} method={method} params={params}")

    if jsonrpc != "2.0" or not method or id_ is None:
        logger.warning(f"Invalid request: jsonrpc={jsonrpc}, method={method}, id={id_}")
        return JSONResponse(
            status_code=200,
            content=jsonrpc_error_response(id_, INVALID_REQUEST),
        )

    handler = METHODS.get(method)
    if not handler:
        logger.warning(f"Method not found: {method} for request id={id_}")
        return JSONResponse(
            status_code=200,
            content=jsonrpc_error_response(id_, METHOD_NOT_FOUND),
        )

    try:
        result = handler(params)
        logger.info(f"Method {method} executed successfully for id={id_}")
    except ValueError as e:
        error_msg = str(e)
        logger.warning(f"Invalid params for method {method} id={id_}: {error_msg}")
        error = {"code": INVALID_PARAMS["code"], "message": error_msg}
        return JSONResponse(
            status_code=200,
            content=jsonrpc_error_response(id_, error),
        )
    except Exception as e:
        logger.error(f"Server error during method {method} request id={id_}: {e}", exc_info=True)
        # Error genérico
        error = {"code": -32000, "message": "Server error"}
        return JSONResponse(
            status_code=200,
            content=jsonrpc_error_response(id_, error),
        )

    response = {
        "jsonrpc": "2.0",
        "id": id_,
        "result": result,
    }
    logger.info(f"Response for request id={id_}: {response}")
    return JSONResponse(content=response)
