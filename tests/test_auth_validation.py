import pytest
from fastapi.testclient import TestClient
from fastapi import status

# Тестовые данные для параметризации
INVALID_LOGIN_PAYLOADS = [

    # Невалидный username
    ("username_too_short", {"username": "us", "password": "password123"}),
    ("username_too_long", {"username": "a" * 51, "password": "password123"}),
    ("username_with_spaces", {"username": "user name", "password": "password123"}),
    ("username_with_special_chars", {"username": "user<name>", "password": "password123"}),

    # Невалидный password
    ("password_too_short", {"username": "testuser", "password": "pass"}),
    ("password_too_long", {"username": "testuser", "password": "p" * 129}),

    # Отсутствующие поля
    ("missing_username", {"password": "password123"}),
    ("missing_password", {"username": "testuser"}),

    # Пустые поля
    ("empty_username", {"username": "", "password": "password123"}), # Не пройдет min_length=3
    ("empty_password", {"username": "testuser", "password": ""}), # Не пройдет min_length=8
]

@pytest.mark.parametrize("scenario, payload", INVALID_LOGIN_PAYLOADS)
def test_login_with_invalid_payload_fails(client: TestClient, scenario: str, payload: dict):
    """
    Проверяет, что запросы на вход с невалидными данными
    возвращают ошибку 422 Unprocessable Entity.
    """
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, f"Failed on scenario: {scenario}"
    data = response.json()
    assert data["title"] == "Validation Error"
    assert "errors" in data
    assert len(data["errors"]) > 0
