from typing import List, Optional, cast

from sqlalchemy.orm import Session

from app.domain.models.entry import Entry as DomainEntry
from app.domain.repositories import AbstractEntryRepository
from app.infrastructure.orm.models import Entry as ORMEntry


class SqlAlchemyEntryRepository(AbstractEntryRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, entry_id: int) -> Optional[DomainEntry]:
        entry_orm = self.session.query(ORMEntry).filter(ORMEntry.id == entry_id).first()
        if not entry_orm:
            return None
        return cast(DomainEntry, DomainEntry.model_validate(entry_orm))

    def list(self, project_id: Optional[int] = None) -> List[DomainEntry]:
        query = self.session.query(ORMEntry)
        if project_id:
            query = query.filter(ORMEntry.project_id == project_id)

        entries_orm = query.all()
        return [DomainEntry.model_validate(e) for e in entries_orm]

    def add(self, entry: DomainEntry) -> DomainEntry:
        entry_orm = ORMEntry(**entry.model_dump())
        self.session.add(entry_orm)
        self.session.commit()
        self.session.refresh(entry_orm)
        return cast(DomainEntry, DomainEntry.model_validate(entry_orm))

    def update(self, entry: DomainEntry) -> DomainEntry:
        entry_orm = self.session.query(ORMEntry).filter(ORMEntry.id == entry.id).first()

        if not entry_orm:
            raise ValueError(f"Entry with id {entry.id} not found")

        entry_data = entry.model_dump(exclude_unset=True)
        for key, value in entry_data.items():
            setattr(entry_orm, key, value)

        self.session.commit()
        self.session.refresh(entry_orm)
        return cast(DomainEntry, DomainEntry.model_validate(entry_orm))

    def delete(self, entry_id: int) -> None:
        entry_orm = self.session.query(ORMEntry).filter(ORMEntry.id == entry_id).first()
        if entry_orm:
            self.session.delete(entry_orm)
            self.session.commit()
