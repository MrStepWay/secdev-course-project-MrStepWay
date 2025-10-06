from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.domain.repositories import AbstractEntryRepository, AbstractProjectRepository
from app.infrastructure.database import get_session_factory
from app.infrastructure.repositories.entry_repository import SqlAlchemyEntryRepository
from app.infrastructure.repositories.project_repository import SqlAlchemyProjectRepository
from app.services.entry_service import EntryService
from app.services.project_service import ProjectService


def get_db() -> Generator[Session, None, None]:
    """Зависимость для получения сессии БД"""
    session_factory = get_session_factory()
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_project_repository(db: Session = Depends(get_db)) -> AbstractProjectRepository:
    return SqlAlchemyProjectRepository(db)


def get_entry_repository(db: Session = Depends(get_db)) -> AbstractEntryRepository:
    return SqlAlchemyEntryRepository(db)


def get_project_service(
    project_repo: AbstractProjectRepository = Depends(get_project_repository),
) -> ProjectService:
    return ProjectService(project_repo=project_repo)


def get_entry_service(
    entry_repo: AbstractEntryRepository = Depends(get_entry_repository),
    project_repo: AbstractProjectRepository = Depends(get_project_repository),
) -> EntryService:
    return EntryService(entry_repo=entry_repo, project_repo=project_repo)
