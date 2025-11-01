from fastapi import status
from fastapi.testclient import TestClient


def test_login_unifies_error_message_to_prevent_enumeration(client: TestClient):
    """
    Тест доказывает, показывающий, что злоумышленник не сможет перебирать логины пользователей.
    Проверяет, что ответы сервера на разные ошибки аутентификации идентичны.
    """

    # Несуществующий пользователь
    response_nonexistent_user = client.post(
        "/api/v1/auth/login", json={"username": "user123", "password": "password123"}
    )

    print(response_nonexistent_user.json())

    assert response_nonexistent_user.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_nonexistent_user.json()["detail"] == "Incorrect username or password"

    # Существующий пользователь, но неверный пароль
    response_wrong_password = client.post(
        "/api/v1/auth/login", json={"username": "testuser", "password": "wrong_password"}
    )
    assert response_wrong_password.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_wrong_password.json()["detail"] == "Incorrect username or password"

    # Проверка, что ответы в обоих сценариях полностью идентичны
    assert response_nonexistent_user.json()["detail"] == response_wrong_password.json()["detail"]


def test_login_blocks_after_too_many_failed_attempts(client: TestClient):
    """
    Проверяет, что после 5 неудачных попыток входа IP-адрес блокируется
    и сервер возвращает ошибку 429 Too Many Requests.
    """
    login_data = {"username": "user_to_be_blocked", "password": "wrong_password"}

    # совершаем 5 неудачных попыток, ожидая код 401
    for i in range(5):
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, f"Attempt {i+1} failed"

    # 6-я попытка должна быть заблокирована
    response_blocked = client.post("/api/v1/auth/login", json=login_data)

    assert response_blocked.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "Retry-After" in response_blocked.headers
