from datetime import datetime
from fastapi.testclient import TestClient


def test_create_project_with_too_long_title_fails(client: TestClient):
    """Название проекта длиннее max_length (100)"""
    long_title = "a" * 1000
    response = client.post("/api/v1/projects/", json={"title": long_title})

    assert response.status_code == 422
    data = response.json()
    errors = data["errors"]

    # Проверяем, что есть ровно одна ошибка
    assert len(errors) == 1
    # Проверяем, что ошибка относится к полю title в теле запроса
    assert errors[0]["loc"] == ["body", "title"]
    # Проверяем тип ошибки
    assert errors[0]["type"] == "string_too_long"


def test_create_project_with_forbidden_chars_fails(client: TestClient):
    """Название проекта содержит запрещенные символы"""
    response = client.post("/api/v1/projects/", json={"title": "Project with <script> tag"})
    assert response.status_code == 422
    data = response.json()
    errors = data["errors"]

    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "title"]
    # Проверяем, что сообщение об ошибке именно то, которое мы задали в валидаторе
    assert "Title must not contain special characters" in errors[0]["msg"]


def test_create_entry_with_negative_duration_fails(client: TestClient):
    """Длительность записи отрицательная"""
    # Сначала создадим проект, чтобы было к чему привязать запись
    project_response = client.post("/api/v1/projects/", json={"title": "Valid Project"})
    project_id = project_response.json()["id"]

    entry_data = {
        "task": "Test Task",
        "started_at": datetime.now().isoformat(),
        "duration_seconds": -100, # Невалидное значение
        "project_id": project_id,
    }
    response = client.post(f"/api/v1/entries/", json=entry_data)

    assert response.status_code == 422
    data = response.json()
    errors = data["errors"]

    assert len(errors) == 1
    assert errors[0]["loc"] == ["body", "duration_seconds"]
    assert "Duration must be a positive number" in errors[0]["msg"]
