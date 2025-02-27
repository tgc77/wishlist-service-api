

from api.routers.router_dispatcher import (
    RequestRouterDispatcher,
    ServiceRouterParameters
)
from api.core.response import APIGatwayProviderResponse


class ProductController:

    async def get_products(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def get_product_by_id(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def get_product_review(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def register_product(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).create(
            service_router_parameters
        )

    async def update_product(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).update(
            service_router_parameters
        )

    async def delete_product(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).delete(
            service_router_parameters
        )
