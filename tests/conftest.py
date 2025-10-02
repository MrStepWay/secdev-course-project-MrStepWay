from typing import Generator, List

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_project_service
from app.domain.models.project import Project
from app.main import app
from app.services.dtos import ProjectCreateDTO


class MockProjectService:
    """
    Сервис, имитирующий интерфейс настоящего ProjectService.
    """

    def __init__(self):
        self.projects: List[Project] = []
        self._next_id = 1

    def get_all_projects(self) -> List[Project]:
        return self.projects

    def create_project(self, project_dto: ProjectCreateDTO) -> Project:
        new_project = Project(id=self._next_id, title=project_dto.title)
        self.projects.append(new_project)
        self._next_id += 1
        return new_project


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Cоздает клиент и управляет жизненным циклом мока."""
    mock_service_instance = MockProjectService()  # Синглтон для каждого теста

    def get_mock_service_override() -> MockProjectService:
        return mock_service_instance

    app.dependency_overrides[get_project_service] = get_mock_service_override

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
