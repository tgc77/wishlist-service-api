
from __future__ import annotations

from json import JSONDecodeError
import json
import sys
from typing import Dict

import httpx
from fastapi import status
from dataclasses import dataclass, field

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from api.core.error_handlers import ResponseExceptionHandler, ResponseHTTPErrorHandler


@dataclass
class ServiceProviderResponse:
    status_code: int = status.HTTP_200_OK
    response: Dict = field(default_factory={})

    @classmethod
    async def from_response(cls, response: Dict, status_code: int = status.HTTP_200_OK) -> ServiceProviderResponse:
        return JSONResponse(
            content=dict(response=response),
            status_code=status_code
        )

    @classmethod
    async def from_exception(cls, exception: ResponseExceptionHandler) -> ServiceProviderResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        content_response = "Bad Request"
        response = exception

        if hasattr(response, 'status_code'):
            status_code = response.status_code

        if hasattr(exception, 'response'):
            response = exception.response
            status_code = response.status_code
        try:
            if response is None:
                return JSONResponse(
                    content=dict(response=content_response),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if hasattr(response, 'json'):
                import inspect
                if not inspect.iscoroutine(response.json):
                    _error_context = response.json()
                else:
                    _error_context = await response.json()
                try:
                    error_context = json.loads(_error_context)
                except:
                    error_context = error_context
            else:
                if hasattr(response, 'message'):
                    error_context = str(response.message).replace("\\", "")
                elif hasattr(response, 'args'):
                    if response.args[0]:
                        error_context = str(response.args[0]).replace("\\", "")
                    else:
                        error_context = str(response).replace("\\", "")
            exception_type, _, _ = sys.exc_info()
            exception_name = getattr(exception_type, "__name__", None)
            content_response = {
                exception_name: error_context
            }
            return JSONResponse(
                content=dict(response=content_response),
                status_code=status_code
            )
        except Exception:
            content_response = jsonable_encoder(response)
            return JSONResponse(
                content=dict(response=content_response),
                status_code=status_code
            )


@dataclass
class APIGatwayProviderResponse:
    status_code: int = status.HTTP_200_OK
    response: Dict = field(default_factory={})

    @classmethod
    async def from_response(cls, response: httpx.Response) -> ServiceProviderResponse:
        try:
            json_response = response.json()
        except (JSONDecodeError, AttributeError):
            json_response = {}
        return JSONResponse(
            content=dict(response=json_response),
            status_code=response.status_code
        )

    @classmethod
    async def from_exception(cls, exception: ResponseHTTPErrorHandler) -> ServiceProviderResponse:
        status_code = status.HTTP_400_BAD_REQUEST
        content_response = "Bad Request"
        response = exception

        if hasattr(response, 'status_code'):
            status_code = response.status_code

        if hasattr(exception, 'response'):
            response = exception.response
            status_code = response.status_code
        try:
            if response is None:
                return JSONResponse(
                    content=dict(response=content_response),
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if hasattr(response, 'json'):
                import inspect
                try:
                    if not inspect.iscoroutine(response.json):
                        error_context = response.json()
                    else:
                        error_context = await response.json()
                except Exception:
                    error_context = response.text
            else:
                if hasattr(response, 'message'):
                    error_context = str(response.message).replace("\\", "")
                elif hasattr(response, 'args'):
                    if response.args[0]:
                        error_context = str(response.args[0]).replace("\\", "")
                    else:
                        error_context = str(response).replace("\\", "")
            exception_type, _, _ = sys.exc_info()
            exception_name = getattr(exception_type, "__name__", None)
            content_response = {
                exception_name: error_context
            }
            return JSONResponse(
                content=dict(response=content_response),
                status_code=status_code
            )
        except Exception:
            try:
                content_response = jsonable_encoder(response)
            except:
                exception_type, _, _ = sys.exc_info()
                exception_name = getattr(exception_type, "__name__", None)
                content_response = {
                    exception_name: error_context or response.args
                }
            return JSONResponse(
                content=dict(response=content_response),
                status_code=status_code
            )
