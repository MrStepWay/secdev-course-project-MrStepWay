from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Глобальная переменная для хранения уже созданной фабрики сессий
_SESSION_FACTORY: Optional[sessionmaker[Session]] = None


def get_session_factory() -> sessionmaker[Session]:
    """
    Возвращает фабрику сессий SQLAlchemy.
    Инициализирует её при первом вызове (ленивая инициализация).
    """
    global _SESSION_FACTORY

    if _SESSION_FACTORY is not None:
        return _SESSION_FACTORY

    if settings.DATABASE_URL is None:
        raise ValueError("DATABASE_URL is not set in the environment or .env file")

    engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)
    _SESSION_FACTORY = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return _SESSION_FACTORY
