from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.orm.base import Base


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


class Entry(Base):
    """
    Модель таблицы с записями.
    """

    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task: Mapped[str] = mapped_column(String(255), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["Project"] = relationship(back_populates="entries")
