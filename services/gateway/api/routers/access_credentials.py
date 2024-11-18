from typing import List
from fastapi import APIRouter, Depends, status
from fastapi_utils.cbv import cbv

from api.core.entities.access_credentials import AccessCredentialsRegister
from api.core.database import AsyncSession, get_async_session
from api.core.logger import logger
from api.core.repositories.access_credentials import AccessCredentialsRepository
from api.core.response import ServiceProviderResponse
from api.core.security.user_authenticator import (
    UserAuthenticator,
    validate_access_credetials_as_admin
)
from api.core.settings import APIConfig


class GatewayAPIAccessCredentialsRoutes:
    prefix: str = APIConfig.ACCESS_CREDENTIALS_PREFIX
    tags: List = ["Access Credentials"]
    get_all: str = '/'
    register: str = '/register'
    update: str = '/update/{client_id}'
    delete: str = '/delete/{client_id}'


access_credentials_router = APIRouter(
    prefix=GatewayAPIAccessCredentialsRoutes.prefix,
    tags=GatewayAPIAccessCredentialsRoutes.tags,
    dependencies=[
        Depends(validate_access_credetials_as_admin)
    ]
)


@cbv(access_credentials_router)
class ServiceGatewayAPIAccessCredentialsRouter:

    @access_credentials_router.get(
        GatewayAPIAccessCredentialsRoutes.get_all,
        response_model=ServiceProviderResponse
    )
    async def get_credentials(
        self,
        session: AsyncSession = Depends(get_async_session)
    ):
        try:
            access_credentials = await AccessCredentialsRepository(session).get_all()
            logger.info("Ouieh! Got Access credentials successfully")
            return await ServiceProviderResponse.from_response(
                response=access_credentials
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )

    @access_credentials_router.post(
        GatewayAPIAccessCredentialsRoutes.register,
        response_model=ServiceProviderResponse
    )
    async def register_credentials(
        self,
        credentials_data: AccessCredentialsRegister,
        session: AsyncSession = Depends(get_async_session)
    ):
        try:
            credentials_register = AccessCredentialsRegister.model_validate(credentials_data)
            await UserAuthenticator(session).register_credentials(access_credentials=credentials_register)
            logger.info("Ouieh! Access credentials created successfully")
            return await ServiceProviderResponse.from_response(
                response={
                    'message': "Access credentials created successfully"
                },
                status_code=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )

    @access_credentials_router.patch(
        GatewayAPIAccessCredentialsRoutes.update,
        response_model=ServiceProviderResponse
    )
    async def update_access_credentials(
        self,
        client_id: int,
        access_credentials: AccessCredentialsRegister,
        session: AsyncSession = Depends(get_async_session)
    ):
        try:
            access_credentials_update = AccessCredentialsRegister.model_validate(access_credentials)
            await AccessCredentialsRepository(session).update(client_id, access_credentials_update)
            logger.info("Ouieh! Access credentials updated successfully")
            return await ServiceProviderResponse.from_response(
                response={
                    'message': "Access credentials updated successfully"
                }
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )

    @access_credentials_router.delete(
        GatewayAPIAccessCredentialsRoutes.delete,
        response_model=ServiceProviderResponse
    )
    async def delete_access_credentials(
        self,
        client_id: int,
        session: AsyncSession = Depends(get_async_session)
    ):
        try:
            await AccessCredentialsRepository(session).delete(client_id=client_id)
            logger.info("Ouieh! Access credentials deleted successfully")
            return await ServiceProviderResponse.from_response(
                response={'message': "Access credentials deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )
