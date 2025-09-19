import json
import os

# Cargar datos mock desde seed.json
seed_path = os.path.join(os.path.dirname(__file__), "seed.json")
with open(seed_path, "r", encoding="utf-8") as f:
    USERS = json.load(f)

def get_user(params):
    user_id = params.get("id")
    if user_id is None:
        raise ValueError("Missing 'id' parameter")
    for user in USERS:
        if user.get("id") == user_id:
            return user
    return None

def search_users(params):
    query = params.get("query", "").lower()
    if not query:
        raise ValueError("Missing or empty 'query' parameter")
    results = [user for user in USERS if query in user.get("name", "").lower()]
    return results

def list_users(params):
    return USERS
