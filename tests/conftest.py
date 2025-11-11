from typing import Generator, List, Optional

import pytest
from fastapi.testclient import TestClient

from app.api.dependencies import get_project_service, get_entry_service
from app.domain.models.project import Project
from app.main import app
from app.services.dtos import ProjectCreateDTO, ProjectUpdateDTO
from app.domain.models.entry import Entry
from app.services.dtos import EntryCreateDTO, EntryUpdateDTO


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


class MockEntryService:
    """Сервис, имитирующий интерфейс EntryService."""
    def __init__(self, project_service: MockProjectService):
        self.entries: List[Entry] = []
        self._next_id = 1
        self.project_service = project_service

    def create_entry(self, entry_dto: EntryCreateDTO) -> Entry:
        # Проверяем существование проекта
        if not self.project_service.get_project_by_id(entry_dto.project_id):
            raise ValueError(f"Project with id {entry_dto.project_id} does not exist.")
        
        # Валидация доменной модели (она сработает до этого теста, но для полноты мока пусть будет)
        new_entry = Entry.model_validate(entry_dto)
        new_entry.id = self._next_id
        
        self.entries.append(new_entry)
        self._next_id += 1
        return new_entry

    def get_all_entries(self, project_id: Optional[int] = None) -> List[Entry]:
        if project_id:
            return [e for e in self.entries if e.project_id == project_id]
        return self.entries


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Фикстура, которая мокает оба сервиса."""
    # Используем существующую фикстуру из conftest для ProjectService
    from app.main import app

    mock_project_service = MockProjectService()
    mock_entry_service = MockEntryService(mock_project_service)

    def get_mock_project_service_override():
        return mock_project_service

    def get_mock_entry_service_override():
        return mock_entry_service

    app.dependency_overrides[get_project_service] = get_mock_project_service_override
    app.dependency_overrides[get_entry_service] = get_mock_entry_service_override

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
