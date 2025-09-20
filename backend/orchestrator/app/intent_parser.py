import re
from typing import Dict, Any

def parse_intent(message: str) -> Dict[str, Any]:
    msg = message.strip().lower()

    # get_user: "usuario 7"
    match = re.match(r"usuario\s+(\d+)", msg)
    if match:
        return {"kind": "get_user", "id": int(match.group(1))}

    # search_users: "buscar ana" o cualquier texto con @ (email)
    match = re.match(r"buscar\s+(.+)", msg)
    if match:
        return {"kind": "search_users", "query": match.group(1).strip()}

    if "@" in msg:
        return {"kind": "search_users", "query": msg}

    # list_users: "lista 3", "últimos 5", "show 10"
    match = re.match(r"(lista|últimos|show)\s+(\d+)", msg)
    if match:
        return {"kind": "list_users", "limit": int(match.group(2))}

    # Ambiguo o no reconocido
    return {"kind": "unknown"}
