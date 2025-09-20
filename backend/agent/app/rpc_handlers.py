from typing import Any, Dict, Optional
from app.data_loader import get_user_by_id, search_users_by_name, list_all_users

def handle_get_user(params: Dict[str, Any]) -> Optional[Dict]:
    user_id = params.get("id")
    if not isinstance(user_id, int):
        raise ValueError("El parámetro 'id' debe ser un entero")
    user = get_user_by_id(user_id)
    return user

def handle_search_users(params: Dict[str, Any]) -> list:
    query = params.get("query")
    if not isinstance(query, str):
        raise ValueError("El parámetro 'query' debe ser una cadena de texto")
    return search_users_by_name(query)

def handle_list_users(params: Dict[str, Any]) -> list:
    # No se esperan parámetros para este método
    return list_all_users()
