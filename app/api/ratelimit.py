import time
from collections import defaultdict
from typing import Dict, List, Tuple

from fastapi import HTTPException, Request, status

from app.api.v1.schemas.auth import UserLoginRequest

# Настройки лимитера
LOGIN_ATTEMPTS_LIMIT = 5
LOGIN_ATTEMPTS_WINDOW_SECONDS = 60
LOGIN_BLOCK_SECONDS = 900  # 15 минут

# In-memory хранилище для неудачных попыток. Временное решение.
# Формат: {(ip, username): [timestamp1, timestamp2, ...]}
_failed_login_attempts: Dict[Tuple[str, str], List[float]] = defaultdict(list)


def record_failed_login(request: Request, form_data: UserLoginRequest):
    """Записывает временную метку неудачной попытки входа."""
    ip = request.client.host if request.client else "unknown"
    username = form_data.username
    key = (ip, username)
    _failed_login_attempts[key].append(time.time())


async def check_rate_limit(request: Request, form_data: UserLoginRequest):
    """
    Зависимость FastAPI для проверки rate limit.
    Блокирует запрос, если превышено количество неудачных попыток.
    """
    ip = request.client.host if request.client else "unknown"
    username = form_data.username
    key = (ip, username)
    current_time = time.time()

    # Отфильтровываем старые временные метки, оставляя только те, что в окне
    valid_attempts = [
        t for t in _failed_login_attempts[key] if current_time - t < LOGIN_ATTEMPTS_WINDOW_SECONDS
    ]
    _failed_login_attempts[key] = valid_attempts

    # Если количество попыток превышает лимит, блокируем
    if len(valid_attempts) >= LOGIN_ATTEMPTS_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed login attempts. Please try again later.",
            headers={"Retry-After": str(LOGIN_BLOCK_SECONDS)},
        )
