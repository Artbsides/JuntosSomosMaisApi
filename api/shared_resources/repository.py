from functools import reduce
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from api.shared_resources.dtos.pagination import PaginationDto


Entity = TypeVar("Entity",
    bound=BaseModel
)


class Respository(Generic[Entity]):
    async def filter(self, data: list[Entity], parameters: BaseModel) -> list[Entity]:
        def matches(entity: Entity, parameters: dict) -> bool:
            for key, value in parameters.items():
                if isinstance(value, dict):
                    if not matches(getattr(entity, key, {}), value):
                        return False
                elif getattr(entity, key) != value:
                    return False

            return True

        return [
            entity for entity in data
                if matches(entity, parameters.model_dump(exclude_none=True, exclude_unset=True))
        ]
    
    async def paginate(self, data: list[Entity], pagination: PaginationDto) -> list[Entity]:
        skip = 0

        if pagination.pageNumber > 0:
            skip = (pagination.pageNumber - 1) * pagination.pageSize

        return data[
            skip:pagination.pageNumber * pagination.pageSize
        ]
