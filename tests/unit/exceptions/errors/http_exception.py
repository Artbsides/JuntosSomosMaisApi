import pytest

from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.exceptions.errors.http_exception import HTTPException
from api.exceptions.errors.internal_server_error import InternalServerError


class TestHTTPException:
    def http_exception_mapped_error_successful_test(self) -> None:
        exception = HTTPException(
            StarletteHTTPException(status_code=status.HTTP_404_NOT_FOUND)
        )

        assert exception.args is not None
        assert exception.status_code is status.HTTP_404_NOT_FOUND

    def http_exception_not_mapped_error_successful_test(self) -> None:
        with pytest.raises(InternalServerError) as exception:
            HTTPException(
                StarletteHTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            )

        assert exception.value.args is not None
        assert exception.value.status_code is status.HTTP_500_INTERNAL_SERVER_ERROR
