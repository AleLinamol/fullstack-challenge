# Códigos de error JSON-RPC estándar
PARSE_ERROR = {"code": -32700, "message": "Parse error"}
INVALID_REQUEST = {"code": -32600, "message": "Invalid Request"}
METHOD_NOT_FOUND = {"code": -32601, "message": "Method not found"}
INVALID_PARAMS = {"code": -32602, "message": "Invalid params"}

def jsonrpc_error_response(id, error):
    return {
        "jsonrpc": "2.0",
        "id": id,
        "error": error
    }
