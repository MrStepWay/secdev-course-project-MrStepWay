from fastapi import status
from fastapi.testclient import TestClient


def test_sql_injection_attempt_via_path_parameter_is_blocked(client: TestClient):
    """
    Проверяет, что попытка SQL-инъекции через
    path-параметр блокируется на уровне валидации FastAPI.

    Ожидается, что FastAPI вернет ошибку 422 Unprocessable Entity,
    поскольку '1 OR 1=1' не является валидным integer.
    """
    # Создаем проект для атаки
    client.post("/api/v1/projects/", json={"title": "Test Project for SQLi"})

    # Формируем вредоносный инпут
    malicious_id = "1 OR 1=1"

    # Делаем запрос с этим инпутом
    response = client.get(f"/api/v1/projects/{malicious_id}")

    # Проверяем, что атака была заблокирована с кодом 422
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Проверяем, что в теле ответа есть информация об ошибке валидации
    data = response.json()
    assert data["title"] == "Validation Error"
    assert "errors" in data
    assert data["errors"][0]["type"] == "int_parsing"
    assert "path" in data["errors"][0]["loc"]
    assert "project_id" in data["errors"][0]["loc"]
