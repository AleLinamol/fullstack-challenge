import pytest
from app.intent_parser import parse_intent

@pytest.mark.parametrize("message, expected_kind", [
    ("usuario 7", "get_user"),
    ("buscar ana", "search_users"),
    ("lista 3", "list_users"),
    ("últimos 5", "list_users"),
    ("show 10", "list_users"),
    ("mensaje desconocido", "unknown"),
    ("", "unknown"),
    ("   ", "unknown"),
    ("correo@ejemplo.com", "search_users"),
])
def test_parse_intent_kinds(message, expected_kind):
    intent = parse_intent(message)
    assert intent["kind"] == expected_kind

def test_parse_intent_params():
    intent = parse_intent("usuario 7")
    assert "id" in intent
    assert intent["id"] == 7

    intent = parse_intent("buscar ana")
    assert "query" in intent
    assert intent["query"] == "ana"

    intent = parse_intent("correo@ejemplo.com")
    assert "query" in intent
    assert intent["query"] == "correo@ejemplo.com"

    intent = parse_intent("lista 3")
    assert "limit" in intent
    assert intent["limit"] == 3

    intent = parse_intent("últimos 5")
    assert "limit" in intent
    assert intent["limit"] == 5

    intent = parse_intent("show 10")
    assert "limit" in intent
    assert intent["limit"] == 10
