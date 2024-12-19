from typing import Dict, List
from sqlmodel import select, text
import uuid as uuid_pkg

from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import and_

from api.core.error_handlers import (
    RegisterNotFound,
    DatabaseIntegrityError,
    UnprocessableEntityException
)
from api.core.entities.favorite_products import FavoriteProductsRegister
from api.core.models.favorite_products import (
    FavoriteProductsModel,
    FavoriteProductsListModel
)
from api.core.models.product import ProductModel
from api.core.logger import logger
from api.core.utils import get_json_pydantic_model
from .repository import Repository


class FavoriteProductsRepository(Repository):
    _favorite_products_model = FavoriteProductsModel
    _favorite_products_list_model = FavoriteProductsListModel
    _product_model = ProductModel

    async def get_client_favorite_products_list(self, client_id: int) -> FavoriteProductsListModel:
        try:
            stmt = select(self._favorite_products_list_model).where(
                self._favorite_products_list_model.client_id == client_id
            )
            result = await self._session.exec(stmt)
            favorite_products_list = result.one()
            return favorite_products_list
        except NoResultFound as ex:
            message = "This client doens't have a favorite product list"
            logger.info(message)
            return None
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get all products: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def create_new_favorite_product_list(self, client_id: int) -> FavoriteProductsListModel:
        try:
            new_favorite_product_list = self._favorite_products_list_model(client_id=client_id)
            self._session.add(new_favorite_product_list)
            await self._session.commit()
            await self._session.refresh(new_favorite_product_list)
            response = new_favorite_product_list
            return response
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong registering new product: {ex}")
            raise DatabaseIntegrityError(error=ex)
        except Exception as ex:
            logger.error(f"Oops! Something went wrong registering new product: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def get_favorite_products_list(self, client_id: int) -> List[Dict]:
        try:
            favorite_product_list = await self.get_client_favorite_products_list(client_id)
            if not favorite_product_list:
                raise NoResultFound("This client doens't have a favorite product list")

            raw_query = """
                SELECT DISTINCT
                    tap.id,
                    tap.title,
                    tap.brand,
                    tap.price,
                    tap.image
                FROM tb_api_product tap
                INNER JOIN tb_api_client_favorite_products tacfp ON tacfp.product_id = tap.id
                INNER JOIN tb_api_client_favorite_products_list tacfpl ON tacfp.favorite_products_list_id = tacfpl.id
                WHERE
                    TRUE
                    AND tacfpl.id=:favorite_products_list_id
            """
            stmt = select(self._product_model).from_statement(text(raw_query))
            result = await self._session.scalars(
                stmt,
                params=dict(
                    favorite_products_list_id=favorite_product_list.id
                )
            )
            products = result.all()
            response = [
                get_json_pydantic_model(product)
                for product in products
            ]
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(message=ex._message())
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get all products: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def get_favorite_product_from_list(
        self,
        client_id: int,
        product_id: uuid_pkg.UUID
    ) -> Dict:
        try:
            favorite_product_list = await self.get_client_favorite_products_list(client_id)
            if not favorite_product_list:
                raise NoResultFound("This client doens't have a favorite product list")

            raw_query = """
                SELECT DISTINCT
                    tap.id,
                    tap.title,
                    tap.brand,
                    tap.price,
                    tap.image
                FROM tb_api_product tap
                INNER JOIN tb_api_client_favorite_products tacfp ON tacfp.product_id = tap.id
                INNER JOIN tb_api_client_favorite_products_list tacfpl ON tacfp.favorite_products_list_id = tacfpl.id
                WHERE
                    TRUE
                    AND tacfpl.id=:favorite_products_list_id
                    AND tacfp.product_id=:product_id
            """
            stmt = select(self._product_model).from_statement(text(raw_query))
            result = await self._session.scalars(
                stmt,
                params=dict(
                    favorite_products_list_id=favorite_product_list.id,
                    product_id=product_id.hex
                )
            )
            product = result.first()
            response = get_json_pydantic_model(product)
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(message=ex._message())
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get all products: {ex}")
            raise UnprocessableEntityException(error=ex)

    async def get_product_by_id(self, id: uuid_pkg.UUID) -> ProductModel:
        try:
            stmt = select(self._product_model).where(self._product_model.id == id)
            result = await self._session.exec(stmt)
            product = result.one()
            response = product
            return response
        except NoResultFound as ex:
            raise RegisterNotFound(error=ex, message=f"The product: {id} doesn't exist")
        except Exception as ex:
            logger.error(f"Oops! Something went wrong to get product with id: {id} => {ex}")
            raise UnprocessableEntityException(error=ex)

    async def include_to_list(self, product_register: FavoriteProductsRegister) -> Dict:
        try:
            favorite_product_list = await self.get_client_favorite_products_list(product_register.client_id)
            if not favorite_product_list:
                favorite_product_list = await self.create_new_favorite_product_list(
                    client_id=product_register.client_id
                )

            if not favorite_product_list:
                raise UnprocessableEntityException(message="Could not create favorite products list")

            product = await self.get_product_by_id(product_register.product_id)
            if not product:
                raise Exception(message=f"Could not verify if product: {product.id} exists")

            product_register.favorite_products_list_id = favorite_product_list.id
            product_to_include = self._favorite_products_model(
                favorite_products_list_id=product_register.favorite_products_list_id,
                product_id=product_register.product_id
            )
            self._session.add(product_to_include)
            await self._session.commit()
            await self._session.refresh(product_to_include)
            response = get_json_pydantic_model(product_to_include)
            return response
        except RegisterNotFound as ex:
            raise RegisterNotFound(message=ex.message)
        except IntegrityError as ex:
            logger.error(f"Oops! Something went wrong: {ex}")
            raise DatabaseIntegrityError(
                error=ex,
                message=f"The product: {product_register.product_id} is already in the favorite products list"
            )
        except Exception as ex:
            logger.error(f"Oops! Something went wrong: {repr(ex)}")
            raise UnprocessableEntityException(error=ex)

    async def remove_favorite_product_from_list(self, client_id: int, product_id: uuid_pkg.UUID):
        try:
            favorite_product_list = await self.get_client_favorite_products_list(client_id)
            if not favorite_product_list:
                raise UnprocessableEntityException(message="Could not get favorite products list")

            product_exist = await self.get_product_by_id(product_id)
            if not product_exist:
                raise Exception(message=f"Could not verify if product: {product_exist.id} exists")

            stmt = select(self._favorite_products_model).where(
                and_(
                    self._favorite_products_model.favorite_products_list_id == favorite_product_list.id,
                    self._favorite_products_model.product_id == product_id
                )
            )
            result = await self._session.exec(stmt)
            favorite_product = result.one()

            if not favorite_product:
                raise NoResultFound(
                    message=f"Product: {favorite_product.product_id} doesn't exists in favorite products list"
                )

            await self._session.delete(favorite_product)
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

    async def delete_favorite_products_list(self, client_id: int):
        try:
            favorite_product_list = await self.get_client_favorite_products_list(client_id)
            if not favorite_product_list:
                raise UnprocessableEntityException(message="Could not get favorite products list")

            await self._session.delete(favorite_product_list)
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
