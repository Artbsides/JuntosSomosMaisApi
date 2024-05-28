from typing import ClassVar
from pydantic import BaseModel

from api.shared_resources.repository import Respository
from api.shared_resources.dtos.pagination import PaginationDto


class TestRepository:
    class Model(BaseModel):
        id: int
        nested: "NestedModel"

        class NestedModel(BaseModel):
            id: int

    data: ClassVar[list[Model]] = [
        Model(id=1, nested=Model.NestedModel(id=1)),
        Model(id=2, nested=Model.NestedModel(id=2))
    ]

    repository = Respository[Model]()

    async def filter_successful_test(self) -> None:
        filtered_data = await self.repository.filter(self.data,
            self.Model(id=1, nested=self.Model.NestedModel(id=1))
        )

        assert len(filtered_data) == 1

        filtered_data = await self.repository.filter(self.data,
            self.Model(id=1, nested=self.Model.NestedModel(id=2))
        )

        assert len(filtered_data) == 0

    async def paginate_successful_test(self) -> None:
        paginated_data = await self.repository.paginate(self.data,
            PaginationDto(pageSize=1, pageNumber=1)
        )

        assert len(paginated_data) == 1
