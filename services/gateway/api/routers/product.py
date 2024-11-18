import uuid as uuid_pkg
from typing import List, Optional
from fastapi import Query, Request, APIRouter
from fastapi_utils.cbv import cbv
import httpx

from api.core.settings import APIConfig
from api.core.logger import logger
from api.core.response import APIGatwayProviderResponse
from api.core.entities.product import (
    ProductRegister,
    ProductUpdate,
    ProductsQueryParams
)
from api.core.security.user_authenticator import (
    AdminAccessAuthorizationHeader,
    ClientAccessAuthorizationHeader
)
from api.core.utils import get_json_pydantic_model


class GatewayAPIProductsRoutes:
    prefix: str = '/products'
    tags: List = ["Products"]
    get_all: str = '/'
    get_by_id: str = '/{id}'
    review: str = '/{id}/review'
    register: str = '/register'
    update: str = '/update/{id}'
    delete: str = '/delete/{id}'


products_router = APIRouter(
    prefix=GatewayAPIProductsRoutes.prefix,
    tags=GatewayAPIProductsRoutes.tags
)


@cbv(products_router)
class ServiceGatewayAPIProductsRouter:

    def __init__(self):
        self.service_url: str = APIConfig.PRODUCTS_SERVICE_URL
        self.route_prefix: str = APIConfig.PRODUCTS_ROUTE_PREFIX
        self.get_products_path = "{service_url}{route_prefix}" + GatewayAPIProductsRoutes.get_all
        self.get_product_by_id_path = "{service_url}{route_prefix}" + GatewayAPIProductsRoutes.get_by_id
        self.get_product_review_path = "{service_url}{route_prefix}" + GatewayAPIProductsRoutes.review
        self.get_register_product_path = "{service_url}{route_prefix}" + GatewayAPIProductsRoutes.register
        self.get_update_product_by_id_path = "{service_url}{route_prefix}" + GatewayAPIProductsRoutes.update
        self.get_delete_product_by_id_path = "{service_url}{route_prefix}" + GatewayAPIProductsRoutes.delete

    def build_route_path(self, route_path: str, **param):
        param.update({'service_url': self.service_url.rstrip('/'), 'route_prefix': self.route_prefix})
        return route_path.format(**param)

    def get_products_route(self) -> str:
        return self.build_route_path(route_path=self.get_products_path)

    def get_product_by_id_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_product_by_id_path, **param)

    def get_product_review_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_product_review_path, **param)

    def get_register_product_route(self) -> str:
        return self.build_route_path(route_path=self.get_register_product_path)

    def get_update_product_by_id_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_update_product_by_id_path, **param)

    def get_delete_product_by_id_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_delete_product_by_id_path, **param)

    @products_router.get(
        GatewayAPIProductsRoutes.get_all,
        response_model=APIGatwayProviderResponse
    )
    async def get_products(
        self,
        request: Request,
        auth_header: ClientAccessAuthorizationHeader,
        limit: Optional[int] = Query(default=20, description="Number of products per page"),
        offset: Optional[int] = Query(default=0, description="Page to search")
    ):
        try:
            query_params = ProductsQueryParams(
                limit=limit,
                offset=offset
            )
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_products_route(),
                headers=auth_header,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                params=query_params.model_dump()
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    @products_router.get(
        GatewayAPIProductsRoutes.get_by_id,
        response_model=APIGatwayProviderResponse
    )
    async def get_product_by_id(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_product_by_id_route(id=id),
                headers=auth_header,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    @products_router.get(
        GatewayAPIProductsRoutes.review,
        response_model=APIGatwayProviderResponse
    )
    async def get_product_review(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_product_review_route(id=id),
                headers=auth_header,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Got response with success")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    @products_router.post(
        GatewayAPIProductsRoutes.register,
        response_model=APIGatwayProviderResponse
    )
    async def register_product(
        self,
        request: Request,
        product_register: ProductRegister,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            new_product = ProductRegister.model_validate(product_register)
            new_product_data = get_json_pydantic_model(new_product)
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.post(
                self.get_register_product_route(),
                json=new_product_data,
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! New product register successfully")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    @products_router.patch(
        GatewayAPIProductsRoutes.update,
        response_model=APIGatwayProviderResponse
    )
    async def update_product(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        product_update: ProductUpdate,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            product = ProductUpdate.model_validate(product_update)
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.patch(
                self.get_update_product_by_id_route(id=id),
                json=get_json_pydantic_model(product),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Product information updated successfully")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    @products_router.delete(
        GatewayAPIProductsRoutes.delete,
        response_model=APIGatwayProviderResponse
    )
    async def delete_product(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.delete(
                self.get_delete_product_by_id_route(id=id),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Product deleted successfully")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )
