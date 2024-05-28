from typing import ClassVar
from fastapi import status

from api.exceptions.errors.api_base_exception import ApiBaseException


class UnauthorizedTokenError(ApiBaseException):
    args: ClassVar[dict[str, str]] = {
        "message": "Check your bearer token, you might not be authorized"
    }

    status_code = status.HTTP_401_UNAUTHORIZED
