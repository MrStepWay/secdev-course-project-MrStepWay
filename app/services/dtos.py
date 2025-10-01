from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

# DTO для проектов
class ProjectCreateDTO(BaseModel):
    title: str = Field(min_length=1, max_length=100)

class ProjectUpdateDTO(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)

# DTO для записей
class EntryCreateDTO(BaseModel):
    task: str = Field(min_length=1, max_length=255)
    started_at: datetime
    duration_seconds: int
    project_id: int

class EntryUpdateDTO(BaseModel):
    task: Optional[str] = Field(None, min_length=1, max_length=255)
    started_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    project_id: Optional[int] = None
