import uuid as uuid_pkg
from typing import Optional
from fastapi import Query, Request
from fastapi_utils.cbv import cbv

from api.core.settings import APIConfig
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
from .router_dispatcher import (
    RequestRouterDispatcher,
    ServiceApiRouter,
    GatewayApiRouter
)

gateway_router = GatewayApiRouter.load_from_apiconfig(APIConfig.PRODUCTS_ROUTES_MAPPER)

service_router = ServiceApiRouter(
    gateway_router=gateway_router,
    service_url=APIConfig.PRODUCTS_SERVICE_URL,
    service_route_prefix=APIConfig.PRODUCTS_ROUTE_PREFIX
)

products_router = service_router.get_app_api_router()


@cbv(products_router)
class ServiceGatewayAPIProductsRouter:

    @products_router.get(
        gateway_router.get_all,
        response_model=APIGatwayProviderResponse
    )
    async def get_products(
        self,
        request: Request,
        auth_header: ClientAccessAuthorizationHeader,
        limit: Optional[int] = Query(default=20, description="Number of products per page"),
        offset: Optional[int] = Query(default=0, description="Page to search")
    ):
        query_params = ProductsQueryParams(
            limit=limit,
            offset=offset
        )
        get_all_router = service_router.get_route_parameters_mapper(gateway_router.get_all)
        get_all_router.auth_header = auth_header
        get_all_router.quey_params = query_params
        return await RequestRouterDispatcher(request).get(
            get_all_router
        )

    @products_router.get(
        gateway_router.get_by,
        response_model=APIGatwayProviderResponse
    )
    async def get_product_by_id(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        get_by_router = service_router.get_route_parameters_mapper(gateway_router.get_by)
        get_by_router.auth_header = auth_header
        get_by_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).get_by(
            get_by_router
        )

    @products_router.get(
        gateway_router.review,
        response_model=APIGatwayProviderResponse
    )
    async def get_product_review(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        auth_header: ClientAccessAuthorizationHeader
    ):
        review_router = service_router.get_route_parameters_mapper(gateway_router.review)
        review_router.auth_header = auth_header
        review_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).get_by(
            review_router
        )

    @products_router.post(
        gateway_router.create,
        response_model=APIGatwayProviderResponse
    )
    async def register_product(
        self,
        request: Request,
        product_register: ProductRegister,
        auth_header: AdminAccessAuthorizationHeader
    ):
        create_router = service_router.get_route_parameters_mapper(gateway_router.create)
        create_router.auth_header = auth_header
        create_router.dispatched_data = product_register
        return await RequestRouterDispatcher(request).create(
            create_router
        )

    @products_router.patch(
        gateway_router.update,
        response_model=APIGatwayProviderResponse
    )
    async def update_product(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        product_update: ProductUpdate,
        auth_header: AdminAccessAuthorizationHeader
    ):
        update_router = service_router.get_route_parameters_mapper(gateway_router.update)
        update_router.auth_header = auth_header
        update_router.dispatched_data = product_update
        update_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).update(
            update_router
        )

    @products_router.delete(
        gateway_router.delete,
        response_model=APIGatwayProviderResponse
    )
    async def delete_product(
        self,
        request: Request,
        id: uuid_pkg.UUID,
        auth_header: AdminAccessAuthorizationHeader
    ):
        delete_router = service_router.get_route_parameters_mapper(gateway_router.delete)
        delete_router.auth_header = auth_header
        delete_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).delete(
            delete_router
        )
