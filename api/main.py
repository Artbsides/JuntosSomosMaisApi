from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from mangum import Mangum

from api.exceptions.exception_handler import ExceptionHandler
from api.modules.states.v1.repository import StatesRepository
from api.modules.users.v1.repository import UsersRepository
from api.routers.router import router
from api.confs.settings import settings
from api.shared_resources.storage import Storage
from api.utils.authorization import Authorization


@asynccontextmanager
async def lifespan(_: FastAPI, storage = Storage()):
    await UsersRepository(
        storage, await StatesRepository(storage).populate()
    ).populate()

    yield


app = FastAPI(
    lifespan=lifespan, dependencies=[
        Depends(Authorization())
    ],
    redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production" else "/docs", debug=settings.APP_DEBUG
)


app.include_router(router)


app.add_exception_handler(Exception, ExceptionHandler.throw)
app.add_exception_handler(HTTPException, ExceptionHandler.throw)
app.add_exception_handler(RequestValidationError, ExceptionHandler.throw)


handler = Mangum(app)
