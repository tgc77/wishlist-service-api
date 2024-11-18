from typing import List
from fastapi import Request, APIRouter
from fastapi_utils.cbv import cbv
import httpx

from api.core.settings import APIConfig
from api.core.logger import logger
from api.core.response import APIGatwayProviderResponse
from api.core.security.user_authenticator import (
    AdminAccessAuthorizationHeader,
    ClientAccessAuthorizationHeader
)
from api.core.entities.client import (
    ClientRegister,
    ClientUpdate,
)


class GatewayAPIClientsRoutes:
    prefix: str = '/clients'
    tags: List = ["Clients"]
    get_all: str = '/'
    get_by_id: str = '/{id}'
    register: str = '/register'
    update: str = '/update/{id}'
    delete: str = '/delete/{id}'


clients_router = APIRouter(
    prefix=GatewayAPIClientsRoutes.prefix,
    tags=GatewayAPIClientsRoutes.tags
)


@cbv(clients_router)
class ServiceGatewayAPIClientsRouter:

    def __init__(self):
        self.service_url: str = APIConfig.CLIENTS_SERVICE_URL
        self.route_prefix: str = APIConfig.CLIENTS_ROUTE_PREFIX
        self.get_clients_path = "{service_url}{route_prefix}" + GatewayAPIClientsRoutes.get_all
        self.get_client_by_id_path = "{service_url}{route_prefix}" + GatewayAPIClientsRoutes.get_by_id
        self.get_register_client_path = "{service_url}{route_prefix}" + GatewayAPIClientsRoutes.register
        self.get_update_client_by_id_path = "{service_url}{route_prefix}" + GatewayAPIClientsRoutes.update
        self.get_delete_client_by_id_path = "{service_url}{route_prefix}" + GatewayAPIClientsRoutes.delete

    def build_route_path(self, route_path: str, **param):
        param.update({'service_url': self.service_url.rstrip('/'), 'route_prefix': self.route_prefix})
        return route_path.format(**param)

    def get_clients_route(self) -> str:
        return self.build_route_path(route_path=self.get_clients_path)

    def get_client_by_id_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_client_by_id_path, **param)

    def get_register_client_route(self) -> str:
        return self.build_route_path(route_path=self.get_register_client_path)

    def get_update_client_by_id_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_update_client_by_id_path, **param)

    def get_delete_client_by_id_route(self, **param) -> str:
        return self.build_route_path(route_path=self.get_delete_client_by_id_path, **param)

    @clients_router.get(
        GatewayAPIClientsRoutes.get_all,
        response_model=APIGatwayProviderResponse
    )
    async def get_clients(
        self,
        request: Request,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_clients_route(),
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

    @clients_router.get(
        GatewayAPIClientsRoutes.get_by_id,
        response_model=APIGatwayProviderResponse
    )
    async def get_client_by_id(
        self,
        request: Request,
        id: int,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.get(
                self.get_client_by_id_route(id=id),
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

    @clients_router.post(
        GatewayAPIClientsRoutes.register,
        response_model=APIGatwayProviderResponse
    )
    async def register_client(
        self,
        request: Request,
        create_client: ClientRegister,
        auth_header: ClientAccessAuthorizationHeader
    ):
        try:
            # TODO testar aqui
            new_client = ClientRegister.model_validate(create_client)
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.post(
                self.get_register_client_route(),
                json=new_client.model_dump(),
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

    @clients_router.patch(
        GatewayAPIClientsRoutes.update,
        response_model=APIGatwayProviderResponse
    )
    async def update_client(
        self,
        request: Request,
        id: int,
        update_client: ClientUpdate,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            client_data = ClientUpdate.model_validate(update_client)
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.patch(
                self.get_update_client_by_id_route(id=id),
                json=client_data.model_dump(),
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

    @clients_router.delete(
        GatewayAPIClientsRoutes.delete,
        response_model=APIGatwayProviderResponse
    )
    async def delete_client(
        self,
        request: Request,
        id: int,
        auth_header: AdminAccessAuthorizationHeader
    ):
        try:
            api_request: httpx.AsyncClient = request.app.api_request
            response = await api_request.delete(
                self.get_delete_client_by_id_route(id=id),
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
