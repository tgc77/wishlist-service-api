from fastapi import Depends, status
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
from .router_dispatcher import (
    ServiceApiRouter,
    GatewayApiRouter
)

gateway_router = GatewayApiRouter.load_from_apiconfig(APIConfig.ACCESS_CREDENTIALS_ROUTES_MAPPER)

service_router = ServiceApiRouter(
    gateway_router=gateway_router,
    service_url=APIConfig.API_GATEWAY_SERVICE_URL
)

access_credentials_router = service_router.get_app_api_router()
access_credentials_router.dependencies = [
    Depends(validate_access_credetials_as_admin)
]


@cbv(access_credentials_router)
class ServiceGatewayAPIAccessCredentialsRouter:

    @access_credentials_router.get(
        gateway_router.get_all,
        response_model=ServiceProviderResponse
    )
    async def get_credentials(self):
        try:
            access_credentials = await AccessCredentialsRepository().get_all()
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
        gateway_router.create,
        response_model=ServiceProviderResponse
    )
    async def register_credentials(
        self,
        credentials_data: AccessCredentialsRegister
    ):
        try:
            credentials_register = AccessCredentialsRegister.model_validate(credentials_data)
            await UserAuthenticator().register_credentials(access_credentials=credentials_register)
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
        gateway_router.update,
        response_model=ServiceProviderResponse
    )
    async def update_access_credentials(
        self,
        client_id: int,
        access_credentials: AccessCredentialsRegister
    ):
        try:
            access_credentials_update = AccessCredentialsRegister.model_validate(access_credentials)
            await AccessCredentialsRepository().update(client_id, access_credentials_update)
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
        gateway_router.delete,
        response_model=ServiceProviderResponse
    )
    async def delete_access_credentials(
        self,
        client_id: int
    ):
        try:
            await AccessCredentialsRepository().delete(client_id=client_id)
            logger.info("Ouieh! Access credentials deleted successfully")
            return await ServiceProviderResponse.from_response(
                response={'message': "Access credentials deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )
