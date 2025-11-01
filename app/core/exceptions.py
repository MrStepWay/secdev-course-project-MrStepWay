from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Маппинг статус-кодов в коды ошибок
HTTP_ERROR_TITLES = {
    status.HTTP_400_BAD_REQUEST: "Bad Request",
    status.HTTP_401_UNAUTHORIZED: "Unauthorized",
    status.HTTP_403_FORBIDDEN: "Forbidden",
    status.HTTP_404_NOT_FOUND: "Not Found",
    status.HTTP_422_UNPROCESSABLE_ENTITY: "Validation Error",
    status.HTTP_429_TOO_MANY_REQUESTS: "Too Many Requests",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
}


async def http_exception_handler(request: Request, exc: Exception):
    """
    Обработчик для стандартных HTTP-ошибок, возвращающий ответ в формате RFC 7807.
    """
    # Гарантируем, что мы работаем с нужным типом исключения
    assert isinstance(exc, StarletteHTTPException)

    correlation_id = str(uuid4())
    status_code = exc.status_code
    title = HTTP_ERROR_TITLES.get(status_code, "Server Error")
    detail = exc.detail

    return JSONResponse(
        status_code=status_code,
        content={
            "type": "about:blank",
            "title": title,
            "status": status_code,
            "detail": detail,
            "correlation_id": correlation_id,
        },
        headers=exc.headers,
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """
    Обработчик для ошибок валидации Pydantic, возвращающий ответ в формате RFC 7807.
    """
    # Гарантируем, что мы работаем с нужным типом исключения
    assert isinstance(exc, RequestValidationError)

    correlation_id = str(uuid4())
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    return JSONResponse(
        status_code=status_code,
        content={
            "type": "about:blank",
            "title": "Validation Error",
            "status": status_code,
            "detail": "Input validation failed. Check the 'errors' field for details.",
            "errors": exc.errors(),
            "correlation_id": correlation_id,
        },
    )


def register_exception_handlers(app: FastAPI):
    """Регистрирует кастомные обработчики исключений."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
