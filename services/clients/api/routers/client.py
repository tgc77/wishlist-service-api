from fastapi import Depends, status, APIRouter
from fastapi_utils.cbv import cbv

from api.core.entities.client import (
    ClientRegister,
    ClientUpdate,
    ClientsView
)
from api.core.security.user_authenticator import JWTBearerAuth
from api.core.database import AsyncSession, get_async_session
from api.core.logger import logger
from api.core.repositories.client import ClientRepository
from api.core.response import ServiceProviderResponse
from api.core.settings import APIConfig

clients_router = APIRouter(
    prefix=APIConfig.CLIENTS_ROUTE_PREFIX,
    tags=["Clients"]
)


@cbv(clients_router)
class ServiceClientsAPIRouter:
    session: AsyncSession = Depends(get_async_session)

    @clients_router.get(
        '/',
        response_model=ServiceProviderResponse,
        dependencies=[Depends(JWTBearerAuth())]
    )
    async def get_clients(self):
        try:
            clients = await ClientRepository(self.session).get_all()
            response = ClientsView(count=len(clients), clients=clients)
            logger.info("Ouieh! Got Clients data successfully!")
            return await ServiceProviderResponse.from_response(response=response.model_dump())
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @clients_router.get(
        '/{id}',
        response_model=ServiceProviderResponse,
        dependencies=[Depends(JWTBearerAuth())]
    )
    async def get_client_by_id(self, id: int):
        try:
            response = await ClientRepository(self.session).get_by_id(id=id)
            logger.info("Ouieh! Got Client data successfully!")
            return await ServiceProviderResponse.from_response(response=response.model_dump())
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @clients_router.post(
        '/register',
        response_model=ServiceProviderResponse
    )
    async def register_client(self, client_register: ClientRegister):
        try:
            response = await ClientRepository(self.session).register(client_register)
            logger.info("Ouieh! Client registerd successfully!")
            return await ServiceProviderResponse.from_response(
                response={'message': "Client registerd successfully!",
                          'client': response.model_dump()},
                status_code=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @clients_router.patch(
        '/update/{id}',
        response_model=ServiceProviderResponse
    )
    async def update_client(self, id: int, client_update: ClientUpdate):
        try:
            response = await ClientRepository(self.session).update(id=id, client_update=client_update)
            logger.info("Ouieh! Client updated successfully!")
            return await ServiceProviderResponse.from_response(
                response={'message': "Client updated successfully!",
                          'client': response.model_dump()}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @clients_router.delete(
        '/delete/{id}',
        response_model=ServiceProviderResponse,
        dependencies=[Depends(JWTBearerAuth())]
    )
    async def delete_client(self, id: int):
        try:
            await ClientRepository(self.session).delete(id=id)
            logger.info("Ouieh! Client deleted successfully!")
            return await ServiceProviderResponse.from_response(
                response={'message': "Client deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)
