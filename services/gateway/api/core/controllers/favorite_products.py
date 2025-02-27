

from api.routers.router_dispatcher import (
    RequestRouterDispatcher,
    ServiceRouterParameters
)
from api.core.response import APIGatwayProviderResponse


class FavoriteProductController:

    async def get_favorite_products_list(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def get_favorite_product_from_list(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def include_favorite_product_to_list(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).create(
            service_router_parameters
        )

    async def remove_favorite_product_from_list(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).delete(
            service_router_parameters
        )

    async def delete_favorite_products_list(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).delete(
            service_router_parameters
        )
