import importlib
import inflection

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from api.exceptions.errors.base import BaseError
from api.exceptions.errors.internal_server import InternalServerError


class ExceptionHandler:
    @staticmethod
    def throw(_: Request, exception: BaseError) -> JSONResponse:
        module = "HTTPExceptionError" if isinstance(exception, HTTPException) \
            else type(exception).__name__

        try:
            exception = getattr(importlib.import_module(
                f"api.exceptions.errors.{ inflection.underscore(module).replace("_error", "") }"), module)(exception)
        except:
            exception = InternalServerError

        response = {
            "data": exception.args
        }

        return JSONResponse(
            response, getattr(exception, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR)
        )
