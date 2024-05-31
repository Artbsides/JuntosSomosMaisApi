import aiohttp

from typing import Type
from fastapi import Depends, status

from api.confs.settings import settings
from api.shared_resources.storage import Storage
from api.shared_resources.repository import Respository
from api.modules.states.v1.dtos.state import StateDto
from api.modules.states.v1.entities.state import State


class StatesRepository(Respository[State]):
    def __init__(self, storage: Storage = Depends()) -> None:
        self.storage = storage

    async def populate(self) -> Type["StatesRepository"]:
        async with aiohttp.ClientSession() as request:
            response = await request.get(
                f"{settings.IBGE_DATA_URL}/estados"
            )

            self.storage.states = (self.storage.states or []) + [
                State(**state)
                    for state in await response.json() if response.status == status.HTTP_200_OK
            ]

        return self

    async def read(self) -> list[State]:
        return self.storage.states or []

    async def read_one(self, parameters: StateDto.ReadOne) -> State:
        return next(filter(
            lambda state: state.name.lower() == parameters.name.lower(),
                await self.read()
            ), None
        )
