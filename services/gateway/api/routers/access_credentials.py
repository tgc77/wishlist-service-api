from fastapi import Depends
from fastapi_utils.cbv import cbv

from api.core.entities.access_credentials import AccessCredentialsRegister
from api.core.response import ServiceProviderResponse
from api.core.security.user_authenticator import (
    validate_access_credetials_as_admin
)
from api.core.settings import APIConfig
from api.core.controllers.access_credentials import AccessCredentialsController
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

    def __init__(self, access_credential_controller: AccessCredentialsController = Depends(AccessCredentialsController)):
        self.access_credential_controller = access_credential_controller

    @access_credentials_router.get(
        gateway_router.get_all,
        response_model=ServiceProviderResponse
    )
    async def get_credentials(self):
        return await self.access_credential_controller.get_credentials()

    @access_credentials_router.post(
        gateway_router.create,
        response_model=ServiceProviderResponse
    )
    async def register_credentials(
        self,
        credentials_data: AccessCredentialsRegister
    ):
        return await self.access_credential_controller.register_credentials(credentials_data=credentials_data)

    @access_credentials_router.patch(
        gateway_router.update,
        response_model=ServiceProviderResponse
    )
    async def update_access_credentials(
        self,
        client_id: int,
        access_credentials: AccessCredentialsRegister
    ):
        return await self.access_credential_controller.update_access_credentials(
            client_id=client_id,
            access_credentials=access_credentials
        )

    @access_credentials_router.delete(
        gateway_router.delete,
        response_model=ServiceProviderResponse
    )
    async def delete_access_credentials(
        self,
        client_id: int
    ):
        return await self.access_credential_controller.delete_access_credentials(client_id=client_id)
