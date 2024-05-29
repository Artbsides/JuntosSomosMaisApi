from fastapi import Request, status
from unittest import mock
from fastapi.responses import JSONResponse

from api.exceptions.errors.not_found import NotFoundError
from api.exceptions.exception_handler import ExceptionHandler


class TestExceptionHandler:
    @mock.patch("api.exceptions.exception_handler.Request")
    def throw_mapped_error_successful_test(self, request: Request) -> None:
        handler = ExceptionHandler.throw(
            request, NotFoundError()
        )

        assert handler.status_code is status.HTTP_404_NOT_FOUND

        assert handler.body is not None
        assert isinstance(handler, JSONResponse)

    @mock.patch("api.exceptions.exception_handler.Request")
    def throw_not_mapped_error_successful_test(self, request: Request) -> None:
        handler = ExceptionHandler.throw(
            request, AttributeError()
        )

        assert handler.status_code is status.HTTP_500_INTERNAL_SERVER_ERROR

        assert handler.body is not None
        assert isinstance(handler, JSONResponse)
