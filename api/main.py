import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException

from api.lifespan import lifespan
from api.confs.settings import settings
from api.routers.router import router
from api.exceptions.exception_handler import ExceptionHandler


app = FastAPI(
    lifespan=lifespan, redoc_url=None, docs_url=None if settings.APP_ENVIRONMENT == "production"
        else "/docs", debug=settings.APP_DEBUG
)


app.include_router(router)

app.add_exception_handler(Exception, ExceptionHandler.throw)
app.add_exception_handler(HTTPException, ExceptionHandler.throw)
app.add_exception_handler(RequestValidationError, ExceptionHandler.throw)


Instrumentator().instrument(app).expose(
    app, tags=["Monitoring"]
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.APP_HOST, port=settings.APP_HOST_PORT
    )
