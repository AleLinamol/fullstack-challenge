import pytest
from app.rpc_handlers import handle_get_user, handle_search_users, handle_list_users
from app.data_loader import users

def test_handle_get_user_valid():
    user = users[0]
    params = {"id": user["id"]}
    result = handle_get_user(params)
    assert result == user
    # Validar campos adicionales
    assert "email" in result
    assert "role" in result
    assert "createdAt" in result

def test_handle_get_user_invalid_id_type():
    params = {"id": "not-an-int"}
    with pytest.raises(ValueError) as excinfo:
        handle_get_user(params)
    assert "id" in str(excinfo.value)

def test_handle_get_user_not_found():
    params = {"id": 999999}  # ID que no existe
    result = handle_get_user(params)
    assert result is None

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
