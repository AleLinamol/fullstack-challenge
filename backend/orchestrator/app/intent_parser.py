import re
from typing import Dict, Any
import unicodedata
import re

def sanitize_text(text: str) -> str:
    # Normalizar unicode (NFKC)
    text = unicodedata.normalize('NFKC', text)
    # Eliminar caracteres no imprimibles
    text = ''.join(ch for ch in text if ch.isprintable())
    # Opcional: eliminar etiquetas HTML o scripts con regex simple
    text = re.sub(r'<[^>]+>', '', text)
    # Limitar longitud
    if len(text) > 200:
        text = text[:200]
    return text

def parse_intent(message: str) -> dict:
    msg = sanitize_text(message).lower().strip()

    if not msg:
        return {"kind": "unknown"}
    # get_user: "usuario 7"
    match = re.match(r"usuario\s+(\d+)$", msg)

    if match:
        return {"kind": "get_user", "id": int(match.group(1))}
    # search_users: "buscar ana" o cualquier texto con @ (email)
    match = re.match(r"buscar\s+(.+)$", msg)

    if match:
        query = match.group(1).strip()
        if query:
            return {"kind": "search_users", "query": query}
        
    if "@" in msg:
        return {"kind": "search_users", "query": msg}
    # list_users: "lista 3", "últimos 5", "show 10"
    match = re.match(r"(lista|últimos|show)\s+(\d+)$", msg)

    if match:
        return {"kind": "list_users", "limit": int(match.group(2))}
    # Ambiguo o no reconocido
    return {"kind": "unknown"}
