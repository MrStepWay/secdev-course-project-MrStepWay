from typing import Generator
from sqlalchemy.orm import Session
from fastapi import Depends
from app.domain.repositories import AbstractProjectRepository, AbstractEntryRepository
from app.infrastructure.database import SessionLocal
from app.infrastructure.repositories.project_repository import SqlAlchemyProjectRepository
from app.infrastructure.repositories.entry_repository import SqlAlchemyEntryRepository
from app.services.project_service import ProjectService
from app.services.entry_service import EntryService

def get_db() -> Generator[Session, None, None]:
    """Зависимость для получения сессии БД"""
    db = SessionLocal()
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
