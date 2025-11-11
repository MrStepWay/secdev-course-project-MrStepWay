from pydantic import BaseModel, Field


class UserLoginRequest(BaseModel):
    """Схема для запроса на вход в систему."""

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_-]+$",  # Разрешены только буквы, цифры, _ и -
        description="Username must be 3-50 characters long and"
        " contain only alphanumeric characters, underscores, and hyphens.",
    )
    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must be at least 8 characters long.",
    )
