from __future__ import annotations

import sys
from typing import Union

import httpx
from fastapi import Request, status, Response
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.responses import JSONResponse, PlainTextResponse


from api.core.logger import logger


class HTTPExceptionHandler(HTTPException, httpx.HTTPStatusError):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, error: Exception, message: str = "") -> None:
        self.error = error
        self.message = message


class ResponseHTTPErrorHandler(HTTPExceptionHandler, Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, error: Exception, message: str = "") -> None:
        super().__init__(error, message)
        self.error = error
        self.message = message


class ResponseExceptionHandler(Exception):

    def __init__(self, error: Exception, message: str = "") -> None:
        self.error = error or self
        self.message = message
        self.status_code: int = status.HTTP_400_BAD_REQUEST
        super().__init__(self.message, self.error, self.status_code)


class RegisterNotFound(ResponseExceptionHandler):

    def __init__(self, error: Exception = None, message: str = "") -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = message or "Register Not Found"
        self.error = error or self
        super().__init__(self.error, self.message)


class RegisterAlreadyExists(ResponseExceptionHandler):

    def __init__(self, error: Exception = None, message: str = "") -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.message = message or "Register Already Exists"
        self.error = error or self
        super().__init__(self.error, self.message)


class DatabaseIntegrityError(ResponseExceptionHandler):

    def __init__(self, error: Exception = None, message: str = "") -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.message = message or "Database Integrity Error"
        self.error = error or self
        super().__init__(self.error, self.message)


class UnprocessableEntityException(ResponseExceptionHandler):

    def __init__(self, error: Exception = None, message: str = "") -> None:
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.message = message or "Unprocessable Entity Exception"
        self.error = error or self
        super().__init__(self.error, self.message)


class UserAccessUnauthorized(ResponseExceptionHandler):

    def __init__(self, error: Exception = None, message: str = "") -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.message = message or "User Access Unauthorized"
        self.error = error or self
        super().__init__(self.error, self.message)


class UserAccessForbidden(ResponseExceptionHandler):

    def __init__(self, error: Exception = None, message: str = "") -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.message = message or "User Access Forbidden"
        self.error = error or self
        super().__init__(self.error, self.message)


async def request_validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    FastAPI wrapper for RequestValidationException handler when API could not catch them.
    This function will be called when client input is not valid.
    """
    logger.info("request_validation_error_handler was invoked")
    body = await request.body()
    query_params = request.query_params._dict
    detail = {"errors": exc.errors(), "body": body.decode(),
              "query_params": query_params}
    logger.info(detail)
    return await request_validation_exception_handler(request, exc)


async def http_error_handler(request: Request, exc: HTTPException) -> Union[JSONResponse, Response]:
    """
    FastAPI wrapper to hendler HTTPException events when API could not catch them.
    This function will be called when a HTTPException is explicitly raised.
    """
    logger.info("http_exception_handler was invoked")
    return await http_exception_handler(request, exc)


async def unhandled_error_handler(request: Request, exc: Exception) -> PlainTextResponse:
    """
    Unhandled exceptions will be logged, sush as HTTPExceptions or RequestValidationErrors
    when API could not catch them.
    """
    host = getattr(getattr(request, "client", None), "host", None)
    port = getattr(getattr(request, "client", None), "port", None)
    url = f"{request.url.path}?{
        request.query_params}" if request.query_params else request.url.path
    exception_type, exception_value, _ = sys.exc_info()
    exception_name = getattr(exception_type, "__name__", None)
    logger.error(
        f"{host}:{port} - {request.method} {url} 500 Internal Server Error "
        f"<{exception_name}: {exception_value}>"
    )
    return PlainTextResponse(str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
