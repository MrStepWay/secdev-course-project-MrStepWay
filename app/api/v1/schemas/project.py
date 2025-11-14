import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProjectBase(BaseModel):
    """
    Базовая схема с общими полями
    """

    title: str = Field(min_length=1, max_length=100)

    @field_validator("title")
    @classmethod
    def title_must_not_contain_special_chars(cls, value: str) -> str:
        """
        Название не должно содержать символы, часто используемые в атаках (XSS и тд).
        """
        if re.search(r"[<>{}]", value):
            raise ValueError("Title must not contain special characters like <, >, {, }")
        return value.strip()


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

    model_config = ConfigDict(from_attributes=True)
