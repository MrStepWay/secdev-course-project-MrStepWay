from fastapi import status
from fastapi.testclient import TestClient


def test_update_project_with_empty_payload_returns_400(client: TestClient):
    """
    Проверяет, что PUT-запрос на обновление проекта с пустым телом
    возвращает ошибку 400, а не 404 или 200.
    Это гарантирует, что клиент должен явно указать, что он хочет изменить.
    """
    # создаём проект, который будем пытаться обновить
    create_response = client.post("/api/v1/projects/", json={"title": "Project to Update"})
    assert create_response.status_code == status.HTTP_201_CREATED
    project_id = create_response.json()["id"]

    # отправляем пустой JSON для обновления
    update_response = client.put(f"/api/v1/projects/{project_id}", json={})

    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    data = update_response.json()

    assert data.get("detail") == "At least one field must be provided for update"
