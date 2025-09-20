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

app = FastAPI()

METHODS = {
    "get_user": handle_get_user,
    "search_users": handle_search_users,
    "list_users": handle_list_users,
}

@app.post("/rpc")
async def rpc_endpoint(request: Request, x_agent_key: str = Header(None)):
    if x_agent_key != AGENT_KEY:
        return JSONResponse(
            status_code=401,
            content={"error": "Unauthorized: Invalid X-Agent-Key header"},
        )

    try:
        payload = await request.json()
    except Exception:
        return JSONResponse(content=jsonrpc_error_response(None, PARSE_ERROR))

    jsonrpc = payload.get("jsonrpc")
    method = payload.get("method")
    params = payload.get("params", {})
    id_ = payload.get("id")

    if jsonrpc != "2.0" or not method or id_ is None:
        return JSONResponse(content=jsonrpc_error_response(id_, INVALID_REQUEST))

    handler = METHODS.get(method)
    if not handler:
        return JSONResponse(content=jsonrpc_error_response(id_, METHOD_NOT_FOUND))

    try:
        result = handler(params)
    except ValueError as e:
        error = {"code": INVALID_PARAMS["code"], "message": str(e)}
        return JSONResponse(content=jsonrpc_error_response(id_, error))
    except Exception:
        # Error genérico
        error = {"code": -32000, "message": "Server error"}
        return JSONResponse(content=jsonrpc_error_response(id_, error))

    response = {
        "jsonrpc": "2.0",
        "id": id_,
        "result": result,
    }
    return JSONResponse(content=response)
