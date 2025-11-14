from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EntryBase(BaseModel):
    """
    Базовая схема
    """

    task: str = Field(min_length=1, max_length=255)
    started_at: datetime
    duration_seconds: int
    project_id: int

    @field_validator("duration_seconds")
    @classmethod
    def duration_must_be_positive(cls, value: int) -> int:
        """
        Валидатор: длительность должна быть положительным числом.
        """
        if value <= 0:
            raise ValueError("Duration must be a positive number of seconds")
        return value


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

    model_config = ConfigDict(from_attributes=True)
