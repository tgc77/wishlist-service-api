from typing import Dict, List
from sqlmodel import select
import uuid as uuid_pkg
from sqlalchemy.exc import NoResultFound, IntegrityError

from api.core.entities.product import ProductEntity
from api.core.database import AsyncSession
from api.core.error_handlers import (
    RegisterNotFound,
    DatabaseIntegrityError,
    UnprocessableEntityException
)
from api.core.models.product import ProductModel
from api.core.logger import logger
from api.core.utils import get_json_pydantic_model
from .repository import Repository


class ProductRepository(Repository):
    _model = ProductModel

    async def get_all_by_filters(self, limit: int, offset: int) -> List[Dict]:
        try:
            page = (offset - 1) if offset > 0 else offset
            _offset = page * limit
            stmt = select(self._model).limit(limit).offset(_offset)
            result = await self._session.exec(stmt)
            products = result.fetchall()
            response = [
                get_json_pydantic_model(product)
                for product in products
            ]
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get all products: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def get_by_id(self, id: uuid_pkg.UUID) -> ProductModel:
        try:
            statement = select(self._model).where(self._model.id == id)
            result = await self._session.exec(statement)
            product = result.one()
            response = product
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get product with id: {id} => {ex}")
            raise UnprocessableEntityException(error=ex)

    async def filter(self, **param) -> List[Dict]:
        try:
            statement = select(self._model).filter(**param)
            result = await self._session.exec(statement)
            products = result.fetchall()
            response = [
                get_json_pydantic_model(product)
                for product in products
            ]
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to fetch product(s): {ex}")
            raise UnprocessableEntityException(error=ex)

    async def register(self, product_register: ProductEntity) -> Dict:
        try:
            new_product = ProductModel(**product_register.model_dump())
            self._session.add(new_product)
            await self._session.commit()
            await self._session.refresh(new_product)
            response = get_json_pydantic_model(new_product)
            return response
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong registering new product: {ex}")
            raise DatabaseIntegrityError(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong registering new product: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def update(self, id: uuid_pkg.UUID, product_update: ProductEntity) -> Dict:
        try:
            product = await self._session.get(self._model, id)
            if not product:
                raise NoResultFound

            product_data = product_update.model_dump(exclude_unset=True)
            product.sqlmodel_update(product_data)
            self._session.add(product)
            await self._session.commit()
            await self._session.refresh(product)
            return get_json_pydantic_model(product)
        except NoResultFound as ex:
            logger.error(f"Oops! Something went wrong updating product: {ex}")
            raise RegisterNotFound(error=ex)
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong updating product: {ex}")
            raise DatabaseIntegrityError(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong updating product: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def delete(self, id: uuid_pkg.UUID):
        try:
            product = await self._session.get(self._model, id)
            if not product:
                raise NoResultFound

            await self._session.delete(product)
            await self._session.commit()
        except NoResultFound as ex:
            logger.error(f"Oops! Something went wrong deleting product: {ex}")
            raise RegisterNotFound(error=ex)
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong deleting product: {ex}")
            raise DatabaseIntegrityError(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong deleting product: {ex}")
            raise UnprocessableEntityException(error=ex)
