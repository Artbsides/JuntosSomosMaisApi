import pytest

from pydantic import ValidationError

from api.shared_resources.dtos.pagination import PaginationDto


class TestPaginationDto:
    def pagination_dto_successful_test(self) -> None:
        dto = PaginationDto()

        assert isinstance(dto.pageSize, int)
        assert isinstance(dto.pageNumber, int)

    def pagination_dto_failure_test(self) -> None:
        with pytest.raises(ValidationError) as exception:
            PaginationDto(pageSize="ten", pageNumber="one")

        assert exception.value.args is not None
