

from api.routers.router_dispatcher import (
    RequestRouterDispatcher,
    ServiceRouterParameters
)
from api.core.response import APIGatwayProviderResponse


class ClientController:

    async def get_clients(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def get_client_by_id(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).get(
            service_router_parameters
        )

    async def register_client(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).create(
            service_router_parameters
        )

    async def update_client(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).update(
            service_router_parameters
        )

    async def delete_client(
        self,
        service_router_parameters: ServiceRouterParameters
    ) -> APIGatwayProviderResponse:
        return await RequestRouterDispatcher(service_router_parameters.request).delete(
            service_router_parameters
        )
