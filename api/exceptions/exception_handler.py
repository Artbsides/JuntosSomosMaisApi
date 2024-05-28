import logging
import importlib
import inflection

from uuid import uuid4
from fastapi import Request, status
from fastapi.responses import JSONResponse

from api.exceptions.errors.internal_server_error import InternalServerError


logger = logging.getLogger("uvicorn")


class ExceptionHandler:
    @staticmethod
    def throw(_: Request, exception: Exception) -> JSONResponse:
        module = type(exception).__name__

        try:
            exception = getattr(importlib.import_module(
                f"api.exceptions.errors.{ inflection.underscore(module) }"), module)(exception)
        except Exception as e:
            exception = InternalServerError(e)

            logger.exception(
                "Application exception: %s", uuid4()
            )

        response = {
            "data": exception.args
        }

        return JSONResponse(
            response, getattr(exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        )
