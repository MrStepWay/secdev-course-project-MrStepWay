from fastapi import APIRouter

from app.api.v1.endpoints import entries, projects

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(entries.router, prefix="/entries", tags=["entries"])
