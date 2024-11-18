
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from contextlib import asynccontextmanager

from api.routers.product import products_router
from api.core.error_handlers import (
    request_validation_error_handler,
    http_error_handler,
    unhandled_error_handler
)


@asynccontextmanager
async def api_initializer(app: FastAPI):
    app.client_request = httpx.AsyncClient()
    yield
    await app.client_request.aclose()

api_description = """
The Amazing LuizaLabs Wishlist Products API
"""

app = FastAPI(
    title="API Products",
    description=api_description,
    summary="Products API to be used in LuizaLabs",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
    },
    lifespan=api_initializer
)

app.include_router(
    products_router
)

app.add_exception_handler(RequestValidationError,
                          request_validation_error_handler)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(Exception, unhandled_error_handler)
