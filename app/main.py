from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.exceptions import register_exception_handlers

app = FastAPI(
    title="Time Tracker API",
    description="API for tracking time spent on projects and tasks.",
    version="1.0.0",
)

register_exception_handlers(app)  # Регистрируем кастомные обработчики ошибок
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["Health Check"])
def health_check():
    """Проверяет, что приложение запущено и отвечает на запросы"""
    return {"status": "ok"}


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Time Tracker API"}
