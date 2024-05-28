from typing import ClassVar
from fastapi import status

from api.exceptions.errors.api_base_exception import ApiBaseException


class InternalServerError(ApiBaseException):
    args: ClassVar[dict[str, str]] = {
        "message": "An internal error occurred"
    }

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
