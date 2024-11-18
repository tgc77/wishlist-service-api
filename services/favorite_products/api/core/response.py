
from __future__ import annotations

import sys
from typing import Dict

import json

from fastapi import status
from dataclasses import dataclass, field

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from api.core.error_handlers import ResponseExceptionHandler


@dataclass
class ServiceProviderResponse:
    response: Dict = field(default_factory={})
    status_code: int = status.HTTP_200_OK

    @classmethod
    async def from_response(cls, response: Dict, status_code: int = status.HTTP_200_OK) -> ServiceProviderResponse:
        return JSONResponse(
            content=response,
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
                    content=content_response,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if hasattr(response, 'json'):
                import inspect
                if not inspect.iscoroutine(response.json):
                    _error_context = response.json()
                else:
                    _error_context = await response.json()
                error_context = json.loads(_error_context)
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
                content=content_response,
                status_code=status_code
            )
        except Exception:
            content_response = jsonable_encoder(response)
            return JSONResponse(
                content=content_response,
                status_code=status_code
            )
