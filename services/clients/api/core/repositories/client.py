from typing import List
from sqlmodel import select

from sqlalchemy.exc import NoResultFound, IntegrityError

from api.core.entities.client import ClientEntity
from api.core.error_handlers import (
    RegisterNotFound,
    RegisterAlreadyExists,
    DatabaseIntegrityError,
    UnprocessableEntityException
)
from api.core.models.client import ClientModel
from api.core.logger import logger
from .repository import Repository


class ClientRepository(Repository):
    _model = ClientModel

    async def get_all(self) -> List[ClientEntity]:
        try:
            result = await self._session.exec(select(self._model))
            clients = result.fetchall()
            response = [
                ClientEntity(**client.model_dump())
                for client in clients
            ]
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(error=ex)
        except Exception as ex:
            logger.error(
                f"Oops! Something went wrong to get all clients: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def get_by_id(self, id: int) -> ClientEntity:
        try:
            statement = select(self._model).where(self._model.id == id)
            result = await self._session.exec(statement)
            client = result.one()
            response = ClientEntity(**client.model_dump())
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(error=ex)
        except Exception as ex:
            logger.error(
                f"Oops! Something went wrong to get client with id: {id} => {ex}")
            raise UnprocessableEntityException(error=ex)

    async def get_by_email(self, email: str) -> ClientEntity:
        try:
            statement = select(self._model).where(self._model.email == email)
            result = await self._session.exec(statement)
            client = result.one()
            response = ClientEntity(**client.model_dump())
            return response
        except NoResultFound as ex:
            raise ex
        except Exception as ex:
            logger.error(
                f"Oops! Something went wrong to get client with email: {email} => {ex}")
            raise UnprocessableEntityException(error=ex)

    async def register(self, client_register: ClientEntity) -> ClientEntity:
        try:
            client = await self.get_by_email(email=client_register.email)
            if client:
                raise RegisterAlreadyExists
        except NoResultFound:
            try:
                new_client = ClientModel(**client_register.model_dump())
                self._session.add(new_client)
                await self._session.commit()
                await self._session.refresh(new_client)
                response = ClientEntity(**new_client.model_dump())
                return response
            except IntegrityError as ex:
                logger.error(
                    f"Oops! Something went wrong register new client: {ex}")
                raise DatabaseIntegrityError(error=ex)
            except Exception as ex:
                logger.error(
                    f"Oops! Something went wrong register new client: {ex}")
                raise UnprocessableEntityException(error=ex)

    async def update(self, id: int, client_update: ClientEntity) -> ClientEntity:
        try:
            client = await self._session.get(self._model, id)
            if not client:
                raise NoResultFound

            client_data = client_update.model_dump(exclude_unset=True)
            client.sqlmodel_update(client_data)
            self._session.add(client)
            await self._session.commit()
            await self._session.refresh(client)
            return ClientEntity(**client.model_dump())
        except NoResultFound as ex:
            logger.error(
                f"Oops! Something went wrong updating client: {ex}")
            raise RegisterNotFound(error=ex)
        except IntegrityError as ex:
            logger.error(
                f"Oops! Something went wrong updating client: {ex}")
            raise DatabaseIntegrityError(error=ex)
        except Exception as ex:
            logger.error(
                f"Oops! Something went wrong updating client: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def delete(self, id: int):
        try:
            client = await self._session.get(self._model, id)
            if not client:
                raise NoResultFound

            await self._session.delete(client)
            await self._session.commit()
        except NoResultFound as ex:
            logger.error(
                f"Oops! Something went wrong deleting client: {ex}")
            raise RegisterNotFound(error=ex)
        except IntegrityError as ex:
            logger.error(
                f"Oops! Something went wrong deleting client: {ex}")
            raise DatabaseIntegrityError(error=ex)
        except Exception as ex:
            logger.error(
                f"Oops! Something went wrong deleting client: {ex}")
            raise UnprocessableEntityException(error=ex)
