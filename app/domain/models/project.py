from pydantic import BaseModel, Field

class Project(BaseModel):
    """
    Доменная модель проекта.
    """
    id: int
    title: str = Field(min_length=1, max_length=100)
    # TODO: owner_id

    class Config:
        from_attributes = True