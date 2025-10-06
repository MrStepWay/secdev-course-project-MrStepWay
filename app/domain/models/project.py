from pydantic import BaseModel, ConfigDict, Field


class Project(BaseModel):
    """
    Доменная модель проекта.
    """

    id: int | None = None
    title: str = Field(min_length=1, max_length=100)
    # TODO: owner_id

    model_config = ConfigDict(from_attributes=True)
