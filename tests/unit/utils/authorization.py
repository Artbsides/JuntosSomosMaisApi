import jwt
import pytest

from fastapi import Request, status
from unittest import mock

from api.confs.settings import settings
from api.utils.authorization import Authorization
from api.exceptions.errors.unauthorized_token_error import UnauthorizedTokenError


class TestAuthorization:
    @mock.patch("api.utils.authorization.Request")
    async def authorization_successful_test(self, request: Request) -> None:
        token = jwt.encode(
            {"exp": 1916239022}, key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
        )

        request.headers = {
            "Authorization": f"Bearer {token}"
        }

        assert await Authorization().__call__(request) is None

    @mock.patch("api.utils.authorization.Request")
    async def authorization_failure_test(self, request: Request) -> None:
        request.headers = {
            "Authorization": "Bearer invalid_token"
        }

        with pytest.raises(UnauthorizedTokenError) as exception:
            await Authorization().__call__(request)

        assert exception.value.args is not None
        assert exception.value.status_code is status.HTTP_401_UNAUTHORIZED
