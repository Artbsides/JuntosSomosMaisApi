from typing import ClassVar
from fastapi import status


class NotFoundError(Exception):
    args: ClassVar[dict[str, str]] = {
        "message": "Resource not found"
    }

    status_code = status.HTTP_404_NOT_FOUND
