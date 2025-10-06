from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Маппинг статус-кодов в коды ошибок
ERROR_CODE_MAP = {
    status.HTTP_400_BAD_REQUEST: "bad_request",
    status.HTTP_401_UNAUTHORIZED: "unauthorized",
    status.HTTP_403_FORBIDDEN: "forbidden",
    status.HTTP_404_NOT_FOUND: "not_found",
    status.HTTP_422_UNPROCESSABLE_ENTITY: "validation_error",
    status.HTTP_500_INTERNAL_SERVER_ERROR: "server_error",
}


async def http_exception_handler(request: Request, exc: Exception):
    """Обработчик для стандартных HTTP-ошибок (HTTPException)."""
    assert isinstance(exc, StarletteHTTPException)

    code = ERROR_CODE_MAP.get(exc.status_code, "server_error")

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": code, "message": exc.detail}},
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """Обработчик для ошибок валидации Pydantic."""
    assert isinstance(exc, RequestValidationError)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "validation_error",
                "message": "Input validation failed",
                "details": exc.errors(),
            }
        },
    )


def register_exception_handlers(app: FastAPI):
    """Регистрирует кастомные обработчики исключений в приложении FastAPI."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
