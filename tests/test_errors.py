import uuid

from fastapi.testclient import TestClient


# Этот тест предполагает, что в проекте уже есть хотя бы один проект,
# чтобы тест на несуществующий ID был валидным.
# Мы создаем его для чистоты теста.
def test_not_found_error_conforms_to_rfc7807(client: TestClient):
    """
    Проверяет, что ошибка 404 Not Found возвращается в формате RFC 7807.
    """
    # создаем проект, чтобы было что не найти
    client.post("/api/v1/projects/", json={"title": "Test Project"})
    non_existent_id = 9999

    # делаем запрос к несуществующему ресурсу
    response = client.get(f"/api/v1/projects/{non_existent_id}")

    assert response.status_code == 404
    data = response.json()

    assert "type" in data
    assert "title" in data
    assert "status" in data
    assert "detail" in data
    assert "correlation_id" in data
    assert data["status"] == 404
    try:
        uuid.UUID(data["correlation_id"])
    except ValueError:
        assert False, "correlation_id is not a valid UUID"


def test_validation_error_conforms_to_rfc7807(client: TestClient):
    """
    Проверяет, что ошибка 422 Unprocessable Entity возвращается в формате RFC 7807.
    """
    response = client.post("/api/v1/projects/", json={"title": 123})

    assert response.status_code == 422
    data = response.json()

    assert "type" in data
    assert data["title"] == "Validation Error"  # Ожидаемый title для ошибок валидации
    assert data["status"] == 422
    assert "detail" in data
    assert "correlation_id" in data

    assert "errors" in data


def test_unhandled_route_error_conforms_to_rfc7807(client: TestClient):
    """
    Проверяет, что ошибка для несуществующего маршрута возвращается в формате RFC 7807.
    """
    response = client.get("/api/v1/this/route/does/not/exist")

    assert response.status_code == 404
    data = response.json()

    assert data["title"] == "Not Found"
    assert data["status"] == 404
    assert "correlation_id" in data
    assert data.get("type") == "about:blank"
