from fastapi import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.exceptions.throws.internal_server_error import InternalServerError
from api.exceptions.throws.not_found import NotFound


class HTTPException(StarletteHTTPException):
    def __new__(self, exception: StarletteHTTPException):
        if exception.status_code == status.HTTP_404_NOT_FOUND:
            return NotFound()

        raise InternalServerError(exception)
