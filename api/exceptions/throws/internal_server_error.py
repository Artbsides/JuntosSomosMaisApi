from fastapi import status


class InternalServerError(Exception):
    args = {
        "message": "An internal error occurred"
    }

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
