import json
from typing import List, Optional, Dict

DATA_FILE = "app/seed.json"

def load_users() -> List[Dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Cargar usuarios al iniciar el módulo para evitar leer archivo en cada consulta
users = load_users()

def get_user_by_id(user_id: int) -> Optional[Dict]:
    return next((user for user in users if user.get("id") == user_id), None)

def search_users_by_name(query: str) -> List[Dict]:
    query_lower = query.lower()
    return [user for user in users if query_lower in user.get("name", "").lower()]

def list_all_users() -> List[Dict]:
    return users
