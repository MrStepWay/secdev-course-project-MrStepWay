from fastapi import status
from fastapi.testclient import TestClient


def test_login_unifies_error_message_to_prevent_enumeration(client: TestClient):
    """
    Тест доказывает, показывающий, что злоумышленник не сможет перебирать логины пользователей.
    Проверяет, что ответы сервера на разные ошибки аутентификации идентичны.
    """
    # Ожидаемый ответ при любой ошибке аутентификации
    expected_error_response = {
        "error": {"code": "unauthorized", "message": "Incorrect username or password"}
    }

    # Несуществующий пользователь
    response_nonexistent_user = client.post(
        "/api/v1/auth/login", json={"username": "user123", "password": "password123"}
    )
    assert response_nonexistent_user.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_nonexistent_user.json() == expected_error_response

    # Существующий пользователь, но неверный пароль
    response_wrong_password = client.post(
        "/api/v1/auth/login", json={"username": "testuser", "password": "wrong_password"}
    )
    assert response_wrong_password.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_wrong_password.json() == expected_error_response

    # Проверка, что ответы в обоих сценариях полностью идентичны
    assert response_nonexistent_user.content == response_wrong_password.content
