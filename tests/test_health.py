from fastapi.testclient import TestClient


def test_create_project_with_mock(client: TestClient):
    """Тест создания проекта."""
    response = client.post("/api/v1/projects/", json={"title": "Mock Project"})

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Mock Project"
    assert data["id"] is not None


def test_get_all_projects_with_mock(client: TestClient):
    """Тест получения списка проектов."""
    # Мок создается заново для каждого теста, поэтому этот тест не увидит данные из предыдущего.

    client.post("/api/v1/projects/", json={"title": "Another Mock Project"})
    response = client.get("/api/v1/projects/")

    assert response.status_code == 200
    data = response.json()
    print(data)
    assert len(data) == 1
    assert data[0]["title"] == "Another Mock Project"
