import json
from typing import List, Optional, Dict

DATA_FILE = "app/seed.json"

def load_users() -> List[Dict]:
    """
    Carga la lista de usuarios desde el archivo JSON.
    Retorna una lista vacía si no se puede leer el archivo.
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar usuarios: {e}")
        return []

# Cargar usuarios al iniciar el módulo para evitar leer archivo en cada consulta
users = load_users()

def get_user_by_id(user_id: int) -> Optional[Dict]:
    """
    Retorna el usuario cuyo 'id' coincida con user_id, o None si no existe.
    """
    return next((user for user in users if user.get("id") == user_id), None)

def search_users(query: str) -> List[Dict]:
    """
    Busca usuarios cuyo nombre o email contengan el texto de búsqueda (case insensitive).
    """
    query_lower = query.lower()
    return [
        user for user in users
        if query_lower in user.get("name", "").lower() or query_lower in user.get("email", "").lower()
    ]

def list_all_users() -> List[Dict]:
    """
    Retorna la lista completa de usuarios.
    """
    return users
