from fastapi import APIRouter

from app.api.v1.endpoints import auth, entries, projects

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(entries.router, prefix="/entries", tags=["entries"])

# Временно. Для демонстрации.
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
