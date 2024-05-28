from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.exceptions.errors.not_found_error import NotFoundError
from api.exceptions.errors.api_base_exception import ApiBaseException
from api.exceptions.errors.internal_server_error import InternalServerError


class HTTPException(ApiBaseException):
    def __new__(cls, exception: StarletteHTTPException) -> ApiBaseException:
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            return NotFoundError()

        raise InternalServerError(exception) from exception
