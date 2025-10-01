from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response

from app.api.dependencies import get_entry_service
from app.api.v1.schemas.entry import EntryCreateRequest, EntryResponse, EntryUpdateRequest
from app.services.dtos import EntryCreateDTO, EntryUpdateDTO
from app.services.entry_service import EntryService

router = APIRouter()


@router.post("/", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(
    entry_in: EntryCreateRequest,
    service: EntryService = Depends(get_entry_service),
):
    entry_dto = EntryCreateDTO(**entry_in.model_dump())
    try:
        entry = service.create_entry(entry_dto)
        return entry
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[EntryResponse])
def get_all_entries(
    project_id: int | None = Query(None, description="Filter entries by project ID"),
    service: EntryService = Depends(get_entry_service),
):
    return service.get_all_entries(project_id=project_id)


@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: int, service: EntryService = Depends(get_entry_service)):
    entry = service.get_entry_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return entry


@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(
    entry_id: int,
    entry_in: EntryUpdateRequest,
    service: EntryService = Depends(get_entry_service),
):
    entry_dto = EntryUpdateDTO(**entry_in.model_dump(exclude_unset=True))
    if not entry_dto.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update",
        )
    try:
        updated_entry = service.update_entry(entry_id, entry_dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    if not updated_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return updated_entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(
    entry_id: int,
    service: EntryService = Depends(get_entry_service),
):
    success = service.delete_entry(entry_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
