from typing import List, Optional

from app.domain.models.entry import Entry
from app.domain.repositories import AbstractEntryRepository, AbstractProjectRepository
from app.services.dtos import EntryCreateDTO, EntryUpdateDTO

class EntryService:
    def __init__(
        self,
        entry_repo: AbstractEntryRepository,
        project_repo: AbstractProjectRepository,
    ):
        self.entry_repo = entry_repo
        self.project_repo = project_repo

    def get_all_entries(self, project_id: Optional[int] = None) -> List[Entry]:
        """Получить все записи, опционально фильтруя по проекту."""
        return self.entry_repo.list(project_id=project_id)

    def get_entry_by_id(self, entry_id: int) -> Optional[Entry]:
        """Получить запись по ID."""
        return self.entry_repo.get(entry_id)

    def create_entry(self, entry_dto: EntryCreateDTO) -> Entry:
        """
        Создать новую запись о времени.
        Проверяет, существует ли указанный проект.
        """
        # Проверяем, существует ли проект
        if not self.project_repo.get(entry_dto.project_id):
            raise ValueError(f"Project with id {entry_dto.project_id} does not exist.")
        
        new_entry_domain = Entry(**entry_dto.model_dump())
        
        created_entry = self.entry_repo.add(new_entry_domain)
        return created_entry

    def update_entry(self, entry_id: int, entry_dto: EntryUpdateDTO) -> Optional[Entry]:
        """Обновить существующую запись."""
        entry_to_update = self.entry_repo.get(entry_id)
        if not entry_to_update:
            return None # Запись не найдена

        update_data = entry_dto.model_dump(exclude_unset=True)

        # Если меняется project_id, нужно проверить его существование
        if "project_id" in update_data:
            if not self.project_repo.get(update_data["project_id"]):
                raise ValueError(f"Project with id {update_data['project_id']} does not exist.")
        
        for key, value in update_data.items():
            setattr(entry_to_update, key, value)
        
        # Повторная валидация после обновления
        validated_entry = Entry.model_validate(entry_to_update)

        updated_entry = self.entry_repo.update(validated_entry)
        return updated_entry

    def delete_entry(self, entry_id: int) -> bool:
        """Удалить запись."""
        entry_to_delete = self.entry_repo.get(entry_id)
        if not entry_to_delete:
            return False # Нечего удалять
        
        self.entry_repo.delete(entry_id)
        return True