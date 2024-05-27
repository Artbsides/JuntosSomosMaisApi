from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.exceptions.throws.internal_server_error import InternalServerError
from api.exceptions.throws.not_found_error import NotFoundError


class HTTPException(StarletteHTTPException):
    def __new__(cls, exception: StarletteHTTPException) -> Exception:
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            return NotFoundError()

        raise InternalServerError(exception) from exception
