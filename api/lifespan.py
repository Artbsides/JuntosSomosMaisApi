from typing import AsyncGenerator
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.shared_resources.storage import Storage
from api.modules.users.v1.repository import UsersRepository
from api.modules.states.v1.repository import StatesRepository


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    storage = Storage()

    await UsersRepository(
        storage, await StatesRepository(storage).populate()
    ).populate()

    yield

    for field in vars(storage):
        setattr(storage, field, None)
