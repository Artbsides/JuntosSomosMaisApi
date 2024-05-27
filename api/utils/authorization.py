import jwt

from typing import Optional
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.confs.settings import settings
from api.exceptions.throws.unauthorized_token_error import UnauthorizedTokenError


class Authorization(HTTPBearer):
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        try:
            authorization = await super().__call__(request)

            jwt.decode(
                authorization.credentials, settings.JWT_SECRET, [settings.JWT_ALGORITHM]
            )

        except Exception as e:
            raise UnauthorizedTokenError from e
