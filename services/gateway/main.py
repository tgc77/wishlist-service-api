
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from contextlib import asynccontextmanager

from api.routers.client import clients_router
from api.routers.product import products_router
from api.routers.favorite_products import favorite_products_router
from api.routers.access_credentials import access_credentials_router
from api.routers.auth import auth_router
# from api.core.initialize_models import create_database_models
from api.core.error_handlers import (
    request_validation_error_handler,
    http_error_handler,
    unhandled_error_handler
)

from api.routers.router_dispatcher import APIServiceRouterManager


@asynccontextmanager
async def api_initializer(app: FastAPI):
    app.api_request = httpx.AsyncClient()
    # await create_database_models()
    yield
    await app.api_request.aclose()

api_description = """
The Amazing LuizaLabs Wishlist Gateway API
"""

app = FastAPI(
    title="API Gateway LuizaLabs Wishlist",
    description=api_description,
    summary="Entry point to the new feature of wishlist to be used in LuizaLabs",
    version="1.0.0",
    contact={
        "name": "Tiago G. Cunha",
        "url": "http://www.linkedin.com/in/tiagogc",
        "email": "tikx.batera@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
    },
    lifespan=api_initializer
)


class InjectCurrentUserMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # TODO: remove it,just for testing
        # app.state.current_user = 'tiago'

        response = await call_next(request)

        if not hasattr(app.state, 'current_user'):
            if hasattr(request.app.state, 'current_user'):
                app.state.current_user = request.app.state.current_user

        return response


app.add_middleware(InjectCurrentUserMiddleware)

app.include_router(clients_router)
app.include_router(products_router)
app.include_router(favorite_products_router)
app.include_router(access_credentials_router)
app.include_router(auth_router)

app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(Exception, unhandled_error_handler)


@app.get("/api/gateway/healthchecker")
def health_checker():
    return {"message": "API is on!"}


# GatewayAPIServiceRouterManager(app=app).register_api_service_router(
#     api_service_router=APIClientsRouter()
# )
