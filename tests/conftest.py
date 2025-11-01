from typing import Generator, List, Optional

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_project_service
from app.domain.models.project import Project
from app.main import app
from app.services.dtos import ProjectCreateDTO, ProjectUpdateDTO


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

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Имитирует получение проекта по ID."""
        for p in self.projects:
            if p.id == project_id:
                return p
        return None

    def update_project(self, project_id: int, project_dto: ProjectUpdateDTO) -> Optional[Project]:
        """Имитирует обновление проекта."""
        project = self.get_project_by_id(project_id)
        if not project:
            return None
        # Обновляем только те поля, что переданы (в нашем случае только title)
        update_data = project_dto.model_dump(exclude_unset=True)
        if "title" in update_data:
            project.title = update_data["title"]
        return project

    def delete_project(self, project_id: int) -> bool:
        """Имитирует удаление проекта."""
        project = self.get_project_by_id(project_id)
        if not project:
            return False
        self.projects.remove(project)
        return True


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Cоздает клиент и управляет жизненным циклом мока."""
    mock_service_instance = MockProjectService()

    def get_mock_service_override() -> MockProjectService:
        return mock_service_instance

    app.dependency_overrides[get_project_service] = get_mock_service_override

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
