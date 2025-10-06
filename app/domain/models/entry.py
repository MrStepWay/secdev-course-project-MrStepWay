from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Entry(BaseModel):
    """
    Доменная модель записи о времени.
    """

    id: int | None = None
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

    model_config = ConfigDict(from_attributes=True)
