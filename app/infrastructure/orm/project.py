from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.orm.base import Base
from app.infrastructure.orm.entry import Entry

class Project(Base):
    """
    Модель таблицы проектов.
    """
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    # Один-ко-многим с каскадным удалением
    entries: Mapped[List["Entry"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
