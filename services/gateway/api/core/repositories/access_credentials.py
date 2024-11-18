from typing import List
from sqlmodel import select

from sqlalchemy.exc import NoResultFound, IntegrityError

from api.core.entities.access_credentials import AccessCredentialsEntity
from api.core.database import AsyncSession
from api.core.error_handlers import (
    RegisterNotFound,
    RegisterAlreadyExists,
    DatabaseIntegrityError,
    UnprocessableEntityException
)
from api.core.models.access_credentials import AccessCredentialsModel
from api.core.security.password_crypt import password_crypt_context
from api.core.logger import logger


class AccessCredentialsRepository:

    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self._model = AccessCredentialsModel

    async def get_all(self) -> List[AccessCredentialsEntity]:
        try:
            statement = select(self._model)
            result = await self._session.exec(statement)
            credentials = result.fetchall()
            users_credentials = [
                user_credentials.model_dump() for user_credentials in credentials
            ]
            response = users_credentials
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(
                error=ex
            )
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get credentials: {ex}")
            raise UnprocessableEntityException(
                error=ex
            )

    async def get_by_username(self, username: str) -> AccessCredentialsEntity:
        try:
            statement = select(self._model).where(
                self._model.username == username
            )
            result = await self._session.exec(statement)
            credential = result.one()
            response = AccessCredentialsEntity(**credential.model_dump())
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(
                error=ex
            )
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get credentials: {ex}")
            raise UnprocessableEntityException(
                error=ex
            )

    async def get_by_client_id(self, client_id: int) -> AccessCredentialsEntity:
        try:
            statement = select(self._model).where(
                self._model.client_id == client_id
            )
            result = await self._session.exec(statement)
            credentials = result.one()
            response = AccessCredentialsEntity(**credentials.model_dump())
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(
                error=ex
            )
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get credentials: {ex}")
            raise UnprocessableEntityException(
                error=ex
            )

    async def register(self, access_credentials_create: AccessCredentialsEntity):
        try:
            access_credentials = await self.get_by_client_id(client_id=access_credentials_create.client_id)
            if access_credentials:
                raise RegisterAlreadyExists
        except RegisterNotFound as ex:
            try:
                new_access_credentials = AccessCredentialsModel(**access_credentials_create.model_dump())
                self._session.add(new_access_credentials)
                await self._session.commit()
                await self._session.refresh(new_access_credentials)
            except IntegrityError as ex:
                logger.error(f"Oops! Something went wrong creating new access credential: {ex}")
                raise DatabaseIntegrityError(
                    error=ex
                )
            except Exception as ex:
                logger.error(f"Oops! Something went wrong creating new access credentials: {ex}")
                raise UnprocessableEntityException(
                    error=ex
                )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return password_crypt_context.verify(plain_password, hashed_password)

    def generate_hashed_password(self, password) -> str:
        return password_crypt_context.hash(password)

    async def update(self, client_id: int, access_credentials_update: AccessCredentialsEntity):
        try:
            access_credentials = await self._session.get(self._model, client_id)
            if not access_credentials:
                raise NoResultFound

            if access_credentials_update.password:
                hashed_password = self.generate_hashed_password(access_credentials_update.password)
                access_credentials_update.password = hashed_password

            credentials_data = access_credentials_update.model_dump(exclude_unset=True)
            access_credentials.sqlmodel_update(credentials_data)
            self._session.add(access_credentials)
            await self._session.commit()
            await self._session.refresh(access_credentials)
        except NoResultFound as ex:
            logger.error(f"Oops! Something went wrong updating access credentials: {ex}")
            raise RegisterNotFound(
                error=ex
            )
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong updating access credentials: {ex}")
            raise DatabaseIntegrityError(
                error=ex,
                message="Client email must be the same as email credentials"
            )
        except Exception as ex:
            logger.error(f"Oops! Something went wrong updating access credentials: {ex}")
            raise UnprocessableEntityException(
                error=ex
            )

    async def delete(self, client_id: int):
        try:
            access_credentials = await self._session.get(self._model, client_id)
            if not access_credentials:
                raise NoResultFound

            await self._session.delete(access_credentials)
            await self._session.commit()
        except NoResultFound as ex:
            logger.error(f"Oops! Something went wrong deleting access credentials: {ex}")
            raise RegisterNotFound(
                error=ex
            )
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong deleting access credentials: {ex}")
            raise DatabaseIntegrityError(
                error=ex
            )
        except Exception as ex:
            logger.error(f"Oops! Something went wrong deleting access credentials: {ex}")
            raise UnprocessableEntityException(
                error=ex
            )
