import jwt
import pytest

from typing import AsyncGenerator
from fastapi import status
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

from api.main import app
from api.lifespan import lifespan
from api.confs.settings import settings
from api.shared_resources.storage import Storage
from api.modules.users.v1.enums.user_types import UserTypesEnum


requests = TestClient(app)


class TestUsersController:
    token = jwt.encode(
        key=settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM, payload={
            "exp": (datetime.now(timezone.utc) + timedelta(seconds=30)).timestamp()
        }
    )

    storage = Storage()

    @pytest.fixture(autouse=True)
    async def _lifespan(self) -> AsyncGenerator[None, None]:
        async with lifespan(app):
            yield

    async def read_successful_test(self) -> None:
        response = requests.get("/users", headers={
                "Authorization": f"Bearer {self.token}"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content is not None

        assert response.json()["totalCount"] == len(self.storage.users)

    async def read_filtered_successful_test(self) -> None:
        parameters = {
            "type": UserTypesEnum.normal.value
        }

        response = requests.get("/users", params=parameters, headers={
                "Authorization": f"Bearer {self.token}"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.content is not None

        assert response.json()["totalCount"] != len(self.storage.users)
