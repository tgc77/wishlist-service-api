from fastapi import Request
from fastapi_utils.cbv import cbv

from api.core.settings import APIConfig
from api.core.response import APIGatwayProviderResponse
from api.core.security.user_authenticator import (
    AdminAccessAuthorizationHeader,
    ClientAccessAuthorizationHeader
)
from api.core.entities.client import (
    ClientRegister,
    ClientUpdate,
)
from .router_dispatcher import (
    RequestRouterDispatcher,
    ServiceApiRouter,
    GatewayApiRouter
)

gateway_router = GatewayApiRouter.load_from_apiconfig(APIConfig.CLIENTS_ROUTES_MAPPER)

service_router = ServiceApiRouter(
    gateway_router=gateway_router,
    service_url=APIConfig.CLIENTS_SERVICE_URL,
    service_route_prefix=APIConfig.CLIENTS_ROUTE_PREFIX
)

clients_router = service_router.get_app_api_router()


@cbv(clients_router)
class APIClientsRouter:

    @clients_router.get(
        gateway_router.get_all,
        response_model=APIGatwayProviderResponse
    )
    async def get_clients(
        self,
        request: Request,
        auth_header: AdminAccessAuthorizationHeader
    ):
        get_all_router = service_router.get_route_parameters_mapper(gateway_router.get_all)
        get_all_router.auth_header = auth_header
        return await RequestRouterDispatcher(request).get(
            get_all_router
        )

    @clients_router.get(
        gateway_router.get_by,
        response_model=APIGatwayProviderResponse
    )
    async def get_client_by_id(
        self,
        request: Request,
        id: int,
        auth_header: AdminAccessAuthorizationHeader
    ):
        get_by_router = service_router.get_route_parameters_mapper(gateway_router.get_by)
        get_by_router.auth_header = auth_header
        get_by_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).get_by(
            get_by_router
        )

    @clients_router.post(
        gateway_router.create,
        response_model=APIGatwayProviderResponse
    )
    async def register_client(
        self,
        request: Request,
        create_client: ClientRegister,
        auth_header: ClientAccessAuthorizationHeader
    ):
        create_router = service_router.get_route_parameters_mapper(gateway_router.create)
        create_router.auth_header = auth_header
        create_router.dispatched_data = create_client
        return await RequestRouterDispatcher(request).create(
            create_router
        )

    @clients_router.patch(
        gateway_router.update,
        response_model=APIGatwayProviderResponse
    )
    async def update_client(
        self,
        request: Request,
        id: int,
        update_client: ClientUpdate,
        auth_header: ClientAccessAuthorizationHeader
    ):
        update_router = service_router.get_route_parameters_mapper(gateway_router.update)
        update_router.auth_header = auth_header
        update_router.dispatched_data = update_client
        update_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).update(
            update_router
        )

    @clients_router.delete(
        gateway_router.delete,
        response_model=APIGatwayProviderResponse
    )
    async def delete_client(
        self,
        request: Request,
        id: int,
        auth_header: AdminAccessAuthorizationHeader
    ):
        delete_router = service_router.get_route_parameters_mapper(gateway_router.delete)
        delete_router.auth_header = auth_header
        delete_router.params = dict(id=id)
        return await RequestRouterDispatcher(request).delete(
            delete_router
        )
