from abc import ABC, abstractmethod
from typing import List, Optional

from .models.entry import Entry
from .models.project import Project


class AbstractProjectRepository(ABC):
    """
    Абстрактный репозиторий (интерфейс) для управления проектами.
    """

    @abstractmethod
    def get(self, project_id: int) -> Optional[Project]:
        """Получить проект по ID."""
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Project]:
        """Получить список всех проектов."""
        raise NotImplementedError

    @abstractmethod
    def add(self, project: Project) -> Project:
        """Добавить новый проект."""
        raise NotImplementedError

    @abstractmethod
    def update(self, project: Project) -> Project:
        """Обновить существующий проект."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_id: int) -> None:
        """Удалить проект по ID."""
        raise NotImplementedError


class AbstractEntryRepository(ABC):
    """
    Абстрактный репозиторий (интерфейс) для управления записями о времени.
    """

    @abstractmethod
    def get(self, entry_id: int) -> Optional[Entry]:
        """Получить запись по ID."""
        raise NotImplementedError

    @abstractmethod
    def list(self, project_id: Optional[int] = None) -> List[Entry]:
        """
        Получить список записей.
        Опционально фильтрует по project_id.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, entry: Entry) -> Entry:
        """Добавить новую запись."""
        raise NotImplementedError

    @abstractmethod
    def update(self, entry: Entry) -> Entry:
        """Обновить существующую запись."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, entry_id: int) -> None:
        """Удалить запись по ID."""
        raise NotImplementedError
