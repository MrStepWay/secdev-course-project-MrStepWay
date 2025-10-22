from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    """Схема для запроса на вход в систему."""

    username: str
    password: str
