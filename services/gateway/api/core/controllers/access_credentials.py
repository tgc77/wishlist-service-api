from fastapi import Depends, status

from api.core.entities.access_credentials import AccessCredentialsRegister
from api.core.logger import logger
from api.core.repositories.access_credentials import AccessCredentialsRepository
from api.core.response import ServiceProviderResponse
from api.core.security.user_authenticator import UserAuthenticator


class AccessCredentialsController:

    def __init__(
        self,
        user_authenticator: UserAuthenticator = Depends(UserAuthenticator),
        access_credentials_repository: AccessCredentialsRepository = Depends(AccessCredentialsRepository)
    ):
        self.user_authenticator = user_authenticator
        self.access_credentials_repository = access_credentials_repository

    async def get_credentials(self):
        try:
            access_credentials = await self.access_credentials_repository.get_all()
            logger.info("Ouieh! Got Access credentials successfully")
            return await ServiceProviderResponse.from_response(
                response=access_credentials
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )

    async def register_credentials(
        self,
        credentials_data: AccessCredentialsRegister
    ):
        try:
            credentials_register = AccessCredentialsRegister.model_validate(credentials_data)
            await self.user_authenticator.register_credentials(access_credentials=credentials_register)
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

    async def update_access_credentials(
        self,
        client_id: int,
        access_credentials: AccessCredentialsRegister
    ):
        try:
            access_credentials_update = AccessCredentialsRegister.model_validate(access_credentials)
            await self.access_credentials_repository.update(client_id, access_credentials_update)
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

    async def delete_access_credentials(
        self,
        client_id: int
    ):
        try:
            await self.access_credentials_repository.delete(client_id=client_id)
            logger.info("Ouieh! Access credentials deleted successfully")
            return await ServiceProviderResponse.from_response(
                response={'message': "Access credentials deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(
                exception=ex
            )
