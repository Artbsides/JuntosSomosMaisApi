import jwt

from typing import Optional

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.confs.settings import settings
from api.exceptions.throws.unauthorized_token_error import UnauthorizedTokenError


class Authorization(HTTPBearer):
    def __init__(self) -> None:
        super(Authorization, self).__init__()

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        try:
            authorization = await super(Authorization, self).__call__(request)

            jwt.decode(
                authorization.credentials, settings.JWT_SECRET, [settings.JWT_ALGORITHM]
            )

        except Exception:
            raise UnauthorizedTokenError
