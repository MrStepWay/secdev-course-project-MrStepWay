from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.orm.base import Base
from app.infrastructure.orm.project import Project

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
