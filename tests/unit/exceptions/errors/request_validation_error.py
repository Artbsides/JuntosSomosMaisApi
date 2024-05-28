from fastapi import status
from fastapi.exceptions import ValidationException

from api.exceptions.errors.request_validation_error import RequestValidationError


class TestRequestValidationError:
    def request_validation_error_successful_test(self) -> None:
        exception = RequestValidationError(
            ValidationException(errors=[{}, {}])
        )

        assert exception.args is not None
        assert exception.status_code is status.HTTP_400_BAD_REQUEST
