from datetime import datetime
from pydantic import BaseModel, Field

class EntryBase(BaseModel):
    """
    Базовая схема
    """
    task: str = Field(min_length=1, max_length=255)
    started_at: datetime
    duration_seconds: int
    project_id: int

class EntryCreateRequest(EntryBase):
    """
    Схема для создания
    """
    pass

class EntryUpdateRequest(BaseModel):
    """
    Схема для обновления
    """
    task: str | None = Field(None, min_length=1, max_length=255)
    started_at: datetime | None = None
    duration_seconds: int | None = None
    project_id: int | None = None

class EntryResponse(EntryBase):
    """
    Схема для ответа
    """
    id: int

    class Config:
        from_attributes = True