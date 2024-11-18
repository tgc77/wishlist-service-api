from typing import List
from fastapi import Request, APIRouter
from fastapi_utils.cbv import cbv
import uuid as uuid_pkg
import httpx

from api.core.settings import APIConfig
from api.core.logger import logger
from api.core.response import APIGatwayProviderResponse
from api.core.entities.favorite_products import FavoriteProductsRegister
from api.core.security.user_authenticator import ClientAccessAuthorizationHeader
from api.core.utils import get_json_pydantic_model


class GatewayAPIFavoriteProductsRoutes:
    prefix: str = '/favorite-products'
    tags: List = ["Favorite Products"]
    get_favorite_products_list: str = '/{client_id}'
    get_favorite_product_from_list: str = '/get-from-list/{client_id}/{product_id}'
    include_favorite_product_to_list: str = '/include-to-list'
    remove_favorite_product_from_list: str = '/remove-from-list/{client_id}/{product_id}'
    delete_favorite_products_list: str = '/delete-list/{client_id}'


favorite_products_router = APIRouter(
    prefix=GatewayAPIFavoriteProductsRoutes.prefix,
    tags=GatewayAPIFavoriteProductsRoutes.tags
)


@cbv(favorite_products_router)
class ServiceGatewayAPIFavoriteProductsRouter:

    def __init__(self):
        self.service_url: str = APIConfig.FAVORITE_PRODUCTS_SERVICE_URL
        self.route_prefix: str = APIConfig.FAVORITE_PRODUCTS_ROUTE_PREFIX
        self.get_favorite_products_list_path = "{service_url}{route_prefix}" + \
            GatewayAPIFavoriteProductsRoutes.get_favorite_products_list
        self.get_favorite_product_from_list_path = "{service_url}{route_prefix}" + \
            GatewayAPIFavoriteProductsRoutes.get_favorite_product_from_list
        self.include_favorite_product_to_list_path = "{service_url}{route_prefix}" + \
            GatewayAPIFavoriteProductsRoutes.include_favorite_product_to_list
        self.remove_favorite_product_from_list_path = "{service_url}{route_prefix}" + \
            GatewayAPIFavoriteProductsRoutes.remove_favorite_product_from_list
        self.delete_favorite_products_list_path = "{service_url}{route_prefix}" + \
            GatewayAPIFavoriteProductsRoutes.delete_favorite_products_list

    def build_route_path(self, route_path: str, **param):
        param.update({'service_url': self.service_url.rstrip('/'), 'route_prefix': self.route_prefix})
        return route_path.format(**param)

    def get_favorite_products_list_route(self, **params):
        return self.build_route_path(route_path=self.get_favorite_products_list_path, **params)

    def get_favorite_product_from_list_route(self, **params):
        return self.build_route_path(route_path=self.get_favorite_product_from_list_path, **params)

    def include_favorite_product_to_list_route(self, **params):
        return self.build_route_path(route_path=self.include_favorite_product_to_list_path, **params)

    def remove_favorite_product_from_list_route(self, **params):
        return self.build_route_path(route_path=self.remove_favorite_product_from_list_path, **params)

    def delete_favorite_products_list_path_route(self, **params):
        return self.build_route_path(route_path=self.delete_favorite_products_list_path, **params)

    @favorite_products_router.get(
        GatewayAPIFavoriteProductsRoutes.get_favorite_products_list,
        response_model=APIGatwayProviderResponse
    )
    async def get_favorite_products_list(
        self,
        request: Request,
        client_id: int,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_favorite_products_list_route(client_id=client_id),
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

    @favorite_products_router.get(
        GatewayAPIFavoriteProductsRoutes.get_favorite_product_from_list,
        response_model=APIGatwayProviderResponse
    )
    async def get_favorite_product_from_list(
        self,
        request: Request,
        client_id: int,
        product_id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_favorite_product_from_list_route(client_id=client_id, product_id=product_id),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=auth_header
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

    @favorite_products_router.post(
        GatewayAPIFavoriteProductsRoutes.include_favorite_product_to_list,
        response_model=APIGatwayProviderResponse
    )
    async def include_favorite_product_to_list(
        self,
        request: Request,
        favorite_product_register: FavoriteProductsRegister,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            new_favorite_product = FavoriteProductsRegister.model_validate(favorite_product_register)
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.post(
                self.include_favorite_product_to_list_route(),
                json=get_json_pydantic_model(new_favorite_product),
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

    @favorite_products_router.delete(
        GatewayAPIFavoriteProductsRoutes.remove_favorite_product_from_list,
        response_model=APIGatwayProviderResponse
    )
    async def remove_favorite_product_from_list(
        self,
        request: Request,
        client_id: int,
        product_id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.delete(
                self.remove_favorite_product_from_list_route(
                    client_id=client_id,
                    product_id=product_id
                ),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Favorite Product removed from list successfully")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )

    @favorite_products_router.delete(
        GatewayAPIFavoriteProductsRoutes.delete_favorite_products_list,
        response_model=APIGatwayProviderResponse
    )
    async def delete_favorite_products_list(
        self,
        request: Request,
        client_id: int,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.delete(
                self.delete_favorite_products_list_path_route(client_id=client_id),
                timeout=APIConfig.HTTP_REQUEST_TIMEOUT,
                headers=auth_header
            )
            response.raise_for_status()
            logger.info(f"Ouieh! Favorite Product List deleted successfully")
            return await APIGatwayProviderResponse.from_response(
                response=response
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await APIGatwayProviderResponse.from_exception(
                exception=ex
            )
