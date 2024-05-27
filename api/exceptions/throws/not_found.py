from fastapi import status


class NotFound(Exception):
    args = {
        "message": "Resource not found"
    }

    status_code = status.HTTP_404_NOT_FOUND
