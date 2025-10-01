from typing import List, Optional

from app.domain.models.project import Project
from app.domain.repositories import AbstractProjectRepository
from app.services.dtos import ProjectCreateDTO, ProjectUpdateDTO

class ProjectService:
    def __init__(self, project_repo: AbstractProjectRepository):
        self.project_repo = project_repo

    def get_all_projects(self) -> List[Project]:
        """Получить все проекты."""
        return self.project_repo.list()

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Получить проект по его ID."""
        project = self.project_repo.get(project_id)
        return project

    def create_project(self, project_dto: ProjectCreateDTO) -> Project:
        """Создать новый проект."""
        new_project_domain = Project(**project_dto.model_dump())
        created_project = self.project_repo.add(new_project_domain)
        return created_project

    def update_project(self, project_id: int, project_dto: ProjectUpdateDTO) -> Optional[Project]:
        """Обновить существующий проект."""
        project_to_update = self.project_repo.get(project_id)
        if not project_to_update:
            return None # Проект не найден
        
        # Обновляем только те поля, которые были переданы в DTO
        update_data = project_dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(project_to_update, key, value)
            
        updated_project = self.project_repo.update(project_to_update)
        return updated_project

    def delete_project(self, project_id: int) -> bool:
        """Удалить проект."""
        project_to_delete = self.project_repo.get(project_id)
        if not project_to_delete:
            return False # Проект не найден, удаления по сути не было
        
        self.project_repo.delete(project_id)
        return True