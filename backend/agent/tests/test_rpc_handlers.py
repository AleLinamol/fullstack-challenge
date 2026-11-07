import pytest
from app.rpc_handlers import handle_get_user, handle_search_users, handle_list_users
from app.data_loader import users

def test_handle_get_user_valid():
    user = users[0]
    params = {"id": user["id"]}
    result = handle_get_user(params)
    assert result == [user]
    # Validar campos adicionales
    assert "email" in result[0]
    assert "role" in result[0]
    assert "createdAt" in result[0]

def test_handle_get_user_invalid_id_type():
    params = {"id": "not-an-int"}
    with pytest.raises(ValueError) as excinfo:
        handle_get_user(params)
    assert "id" in str(excinfo.value)

def test_handle_get_user_not_found():
    params = {"id": 999999}  # ID que no existe
    result = handle_get_user(params)
    assert result == []

def test_handle_search_users_valid():
    # Buscar por nombre parcial, case insensitive
    params = {"query": "ana"}
    result = handle_search_users(params)
    assert isinstance(result, list)
    assert any("ana" in user["name"].lower() for user in result)
    # Validar campos adicionales en resultados
    for user in result:
        assert "email" in user
        assert "role" in user
        assert "createdAt" in user

def test_search_users_by_email():
    params = {"query":"@elogia.tech"}
    result = handle_search_users(params)
    assert isinstance(result, list)
    assert any("ana" in user["name"].lower() for user in result)
    # Validar campos adicionales en resultados
    for user in result:
        assert "name" in user
        assert "role" in user
        assert "createdAt" in user


def test_handle_search_users_invalid_query_type():
    params = {"query": 123}
    with pytest.raises(ValueError) as excinfo:
        handle_search_users(params)
    assert "query" in str(excinfo.value)

def test_handle_list_users():
    params = {}
    result = handle_list_users(params)
    assert isinstance(result, list)
    assert len(result) == len(users)
    # Validar campos adicionales en todos los usuarios
    for user in result:
        assert "email" in user
        assert "role" in user
        assert "createdAt" in user


def test_list_too_large_remains_an_error_with_friendly_message():
    requested = len(users) + 5
    with pytest.raises(ValueError) as excinfo:
        handle_list_users({"limit": requested})
    assert str(excinfo.value) == f"Pediste {requested} usuarios, pero por ahora solo hay {len(users)} disponibles. Probá con «lista {len(users)}»."


def test_list_empty_directory_remains_an_error(monkeypatch):
    monkeypatch.setattr("app.rpc_handlers.list_all_users", lambda: [])
    with pytest.raises(ValueError, match="Todavía no hay usuarios cargados"):
        handle_list_users({"limit": 10})


def test_list_single_user_error_uses_singular(monkeypatch):
    monkeypatch.setattr("app.rpc_handlers.list_all_users", lambda: [users[0]])
    with pytest.raises(ValueError, match="solo hay 1 disponible"):
        handle_list_users({"limit": 10})
