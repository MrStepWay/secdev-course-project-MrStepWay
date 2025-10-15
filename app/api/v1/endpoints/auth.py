from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# Временные моки для демонстрации
FAKE_USERS_DB = {"testuser": "hashed_password_for_testuser"}


def verify_password(plain_password, hashed_password):
    # В реальности здесь будет что-то типа passlib.verify()
    return hashed_password == f"hashed_password_for_{plain_password}"


class UserLoginRequest(BaseModel):
    username: str
    password: str


# Безопасная реализация (только в целях демонстрации)
@router.post("/login", tags=["auth"])
def login_secure(form_data: UserLoginRequest):
    """
    Безопасный эндпоинт: всегда возвращает общую ошибку,
    чтобы нельзя было перебирать логины пользователей.
    """
    user_password_hash = FAKE_USERS_DB.get(form_data.username)

    # Создаем общее исключение, которое будем вызывать в любом случае ошибки
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user_password_hash or not verify_password(form_data.password, user_password_hash):
        raise credentials_exception

    return {"access_token": form_data.username, "token_type": "bearer"}
