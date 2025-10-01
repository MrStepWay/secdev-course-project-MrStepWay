from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from app.api.dependencies import get_project_service
from app.api.v1.schemas.project import ProjectCreateRequest, ProjectResponse, ProjectUpdateRequest
from app.services.dtos import ProjectCreateDTO, ProjectUpdateDTO
from app.services.project_service import ProjectService

router = APIRouter()

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreateRequest,
    service: ProjectService = Depends(get_project_service),
):
    project_dto = ProjectCreateDTO(**project_in.model_dump())
    project = service.create_project(project_dto)
    return project

@router.get("/", response_model=List[ProjectResponse])
def get_all_projects(service: ProjectService = Depends(get_project_service)):
    return service.get_all_projects()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_in: ProjectUpdateRequest,
    service: ProjectService = Depends(get_project_service),
):
    project_dto = ProjectUpdateDTO(**project_in.model_dump())
    updated_project = service.update_project(project_id, project_dto)
    if not updated_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return updated_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    service: ProjectService = Depends(get_project_service),
):
    success = service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
