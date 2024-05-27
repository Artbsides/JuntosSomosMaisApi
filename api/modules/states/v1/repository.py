import requests

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
        self.storage.states = await \
            self.read()

        return self

    async def read(self) -> list[State]:
        if self.storage.states:
            return self.storage.states

        response = requests.get(
            f"{settings.IBGE_DATA_URL}/estados"
        )

        return [
            State(**state)
                for state in response.json()
        ] if response.status_code == status.HTTP_200_OK else []

    async def read_one(self, parameters: StateDto.ReadOne) -> State:
        return next(filter(
            lambda state: state.name.lower() == parameters.name.lower(),
                self.storage.states
            ), None
        )
