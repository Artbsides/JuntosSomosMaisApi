from fastapi import status


class UnauthorizedTokenError(Exception):
    args = {
        "message": "Check your bearer token, you might not be authorized"
    }

    status_code = status.HTTP_401_UNAUTHORIZED
