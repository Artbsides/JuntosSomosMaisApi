import csv
import requests

from typing import Optional, Type
from fastapi import Depends, status

from api.modules.states.v1.dtos.state import StateDto
from api.modules.states.v1.repository import StatesRepository
from api.modules.users.v1.dtos.user import UserDto
from api.modules.users.v1.entities.user import User
from api.shared_resources.entities.paginated import Paginated
from api.shared_resources.repository import Respository
from api.shared_resources.storage import Storage
from api.utils.format_data import FormatData
from api.confs.settings import settings


class UsersRepository(Respository[User]):
    def __init__(self, storage: Storage = Depends(), states_repository: StatesRepository = Depends()) -> None:
        self.storage = storage
        self.states_repository = states_repository

    async def populate(self) -> Type["UsersRepository"]:
        for file_extension in ["json", "csv"]:
            response = requests.get(
                f"{settings.JSM_DATA_URL}/input-backend.{file_extension}"
            )

            if response.status_code == status.HTTP_200_OK:
                users: Optional[list[dict]] = None

                if file_extension == "json":
                    users = response.json()["results"]

                else:
                    users = FormatData.nested_dicts(list(
                        csv.DictReader(
                            response.content.decode("utf-8-sig").splitlines()
                        )
                    ))

                for user in users:
                    user["location"]["region"] = (
                        await self.states_repository
                            .read_one(StateDto.ReadOne(name=user["location"]["state"]))
                    ).region

                    self.storage.users = (self.storage.users or []) + [User(**user)]

        return self

    async def read(self, parameters: UserDto.Read) -> Paginated[User]:
        users = await self.filter(
            self.storage.users, parameters.filters
        )

        return Paginated[User](
            **{**parameters.pagination.model_dump(), "totalCount": len(users)},
                data = await self.paginate(users, parameters.pagination)
        )
