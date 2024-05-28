from typing import ClassVar
from pydantic import BaseModel

from api.shared_resources.entities.paginated import Paginated


class TestPaginated:
    class Model(BaseModel):
        id: int

    data: ClassVar[list[Model]] = [
        Model(id=1),
        Model(id=2)
    ]

    def paginated_successful_test(self) -> None:
        entity = Paginated[self.Model](
            data=self.data, pageSize=1, pageNumber=1
        )

        assert len(entity.data) == len(self.data)
