from typing import Any, Dict, Optional, List
from app.data_loader import get_user_by_id, search_users, list_all_users

def handle_get_user(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    user_id = params.get("id")
    if not isinstance(user_id, int):
        raise ValueError("El parámetro 'id' debe ser un entero")
    user = get_user_by_id(user_id)
    if user is None:
        return []
    return [user]

def handle_search_users(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    query = params.get("query")
    if not isinstance(query, str):
        raise ValueError("El parámetro 'query' debe ser una cadena de texto")
    return search_users(query)

def handle_list_users(params: Dict[str, Any]) -> List[Dict[str, Any]]:
    limit = params.get("limit")
    all_users = list_all_users()
    total_users = len(all_users)
    
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("El parámetro 'limit' debe ser un entero no negativo")
        if limit > total_users:
            if total_users == 0:
                raise ValueError("Todavía no hay usuarios cargados en este directorio. Probá nuevamente más adelante.")
            available = "1 disponible" if total_users == 1 else f"{total_users} disponibles"
            raise ValueError(f"Pediste {limit} usuarios, pero por ahora solo hay {available}. Probá con «lista {total_users}».")
        return all_users[:limit]
    
    return all_users




