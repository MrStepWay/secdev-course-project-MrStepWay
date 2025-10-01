from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    """
    Базовая схема с общими полями
    """
    title: str = Field(min_length=1, max_length=100)

class ProjectCreateRequest(ProjectBase):
    """
    Схема для создания проекта (получаем от клиента)
    """
    pass

class ProjectUpdateRequest(BaseModel):
    """
    Схема для обновления (тело PUT запроса)
    """
    title: str | None = Field(None, min_length=1, max_length=100)

class ProjectResponse(ProjectBase):
    """
    Схема для ответа API
    """
    id: int

    class Config:
        from_attributes = True