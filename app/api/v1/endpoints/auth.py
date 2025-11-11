from fastapi import APIRouter, Depends, HTTPException, Request, status
import logging

from app.api.ratelimit import check_rate_limit, record_failed_login
from app.api.v1.schemas.auth import UserLoginRequest

router = APIRouter()
logger = logging.getLogger(__name__)

# Временные моки для демонстрации
FAKE_USERS_DB = {"testuser": "hashed_password_for_testuser"}


def verify_password(plain_password, hashed_password):
    return hashed_password == f"hashed_password_for_{plain_password}"


@router.post("/login", tags=["auth"], dependencies=[Depends(check_rate_limit)])
def login_secure(request: Request, form_data: UserLoginRequest):
    """
    Безопасный эндпоинт: всегда возвращает общую ошибку,
    чтобы нельзя было перебирать логины пользователей.
    Защищен от брутфорса с помощью rate limiting.
    """
    user_password_hash = FAKE_USERS_DB.get(form_data.username)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not user_password_hash or not verify_password(form_data.password, user_password_hash):
        log_data = {"event": "login_failed", "username": form_data.username, "password": form_data.password}
        logger.warning("Failed login attempt", extra={"data": log_data})

        # Перед тем как выбросить ошибку, фиксируем неудачную попытку
        record_failed_login(request, form_data)
        raise credentials_exception
    
    logger.info(f"User '{form_data.username}' logged in successfully.", extra={"data": {"username": form_data.username}})

    return {"access_token": form_data.username, "token_type": "bearer"}
