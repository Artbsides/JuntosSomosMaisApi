from typing import Generic, TypeVar
from pydantic import Field, BaseModel


Entity = TypeVar("Entity")


class Paginated(BaseModel, Generic[Entity]):
    data: list[Entity]
    pageSize: int = Field(ge=1)
    pageNumber: int = Field(ge=1)
    totalCount: int = 0
