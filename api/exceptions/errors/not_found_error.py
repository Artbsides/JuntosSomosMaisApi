from typing import ClassVar
from fastapi import status

from api.exceptions.errors.api_base_exception import ApiBaseException


class NotFoundError(ApiBaseException):
    args: ClassVar[dict[str, str]] = {
        "message": "Resource not found"
    }

    status_code = status.HTTP_404_NOT_FOUND
