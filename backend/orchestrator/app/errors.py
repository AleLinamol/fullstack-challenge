class JSONRPCError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(f"JSON-RPC Error {code}: {message}")
        self.code = code
        self.message = message
