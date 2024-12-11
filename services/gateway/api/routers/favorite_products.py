from fastapi import Request
from fastapi_utils.cbv import cbv
import uuid as uuid_pkg

from api.core.settings import APIConfig
from api.core.response import APIGatwayProviderResponse
from api.core.entities.favorite_products import FavoriteProductsRegister
from api.core.security.user_authenticator import ClientAccessAuthorizationHeader
from .router_dispatcher import (
    RequestRouterDispatcher,
    ServiceApiRouter,
    GatewayApiRouter
)

gateway_router = GatewayApiRouter.load_from_apiconfig(APIConfig.FAVORITE_PRODUCTS_ROUTES_MAPPER)

service_router = ServiceApiRouter(
    gateway_router=gateway_router,
    service_url=APIConfig.FAVORITE_PRODUCTS_SERVICE_URL,
    service_route_prefix=APIConfig.FAVORITE_PRODUCTS_ROUTE_PREFIX
)

favorite_products_router = service_router.get_app_api_router()


@cbv(favorite_products_router)
class ServiceGatewayAPIFavoriteProductsRouter:

    @favorite_products_router.get(
        gateway_router.get_all,
        response_model=APIGatwayProviderResponse
    )
    async def get_favorite_products_list(
        self,
        request: Request,
        client_id: int,
        auth_header: ClientAccessAuthorizationHeader
    ):
        get_all_router = service_router.get_route_parameters_mapper(gateway_router.get_all)
        get_all_router.auth_header = auth_header
        get_all_router.params = dict(client_id=client_id)
        return await RequestRouterDispatcher(request).get(
            get_all_router
        )

    @favorite_products_router.get(
        gateway_router.get_by,
        response_model=APIGatwayProviderResponse
    )
    async def get_favorite_product_from_list(
        self,
        request: Request,
        client_id: int,
        product_id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        get_by_router = service_router.get_route_parameters_mapper(gateway_router.get_by)
        get_by_router.auth_header = auth_header
        get_by_router.params = dict(
            client_id=client_id,
            product_id=product_id
        )
        return await RequestRouterDispatcher(request).get_by(
            get_by_router
        )

    @favorite_products_router.post(
        gateway_router.create,
        response_model=APIGatwayProviderResponse
    )
    async def include_favorite_product_to_list(
        self,
        request: Request,
        favorite_product_register: FavoriteProductsRegister,
        auth_header: ClientAccessAuthorizationHeader
    ):
        create_router = service_router.get_route_parameters_mapper(gateway_router.create)
        create_router.auth_header = auth_header
        create_router.dispatched_data = favorite_product_register
        return await RequestRouterDispatcher(request).create(
            create_router
        )

    @favorite_products_router.delete(
        gateway_router.delete['from-list'],
        response_model=APIGatwayProviderResponse
    )
    async def remove_favorite_product_from_list(
        self,
        request: Request,
        client_id: int,
        product_id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        delete_router = service_router.get_route_parameters_mapper(gateway_router.delete['from-list'])
        delete_router.auth_header = auth_header
        delete_router.params = dict(
            client_id=client_id,
            product_id=product_id
        )
        return await RequestRouterDispatcher(request).delete(
            delete_router
        )

    @favorite_products_router.delete(
        gateway_router.delete['list'],
        response_model=APIGatwayProviderResponse
    )
    async def delete_favorite_products_list(
        self,
        request: Request,
        client_id: int,
        auth_header: ClientAccessAuthorizationHeader
    ):
        delete_router = service_router.get_route_parameters_mapper(gateway_router.delete['list'])
        delete_router.auth_header = auth_header
        delete_router.params = dict(
            client_id=client_id
        )
        return await RequestRouterDispatcher(request).delete(
            delete_router
        )
