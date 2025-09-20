from app.errors import (
    PARSE_ERROR,
    INVALID_REQUEST,
    METHOD_NOT_FOUND,
    INVALID_PARAMS,
    jsonrpc_error_response,
)

def test_error_constants():
    assert PARSE_ERROR["code"] == -32700
    assert INVALID_REQUEST["code"] == -32600
    assert METHOD_NOT_FOUND["code"] == -32601
    assert INVALID_PARAMS["code"] == -32602

def test_jsonrpc_error_response_structure():
    error = {"code": -32000, "message": "Server error"}
    response = jsonrpc_error_response(123, error)
    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 123
    assert response["error"] == error
