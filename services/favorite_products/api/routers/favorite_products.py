from fastapi import Depends, status, APIRouter
from fastapi_utils.cbv import cbv
import uuid as uuid_pkg

from api.core.entities.favorite_products import (
    FavoriteProductsRegister,
    FavoriteProductsListView,
    FavoriteProductView
)
from api.core.security.user_authenticator import JWTBearerAuth
from api.core.logger import logger
from api.core.repositories.favorite_products import FavoriteProductsRepository
from api.core.response import ServiceProviderResponse
from api.core.settings import APIConfig
from .route_mapper import ServiceApiRouteMapper


favorite_products_routes_mapper = ServiceApiRouteMapper.load_from_apiconfig(
    APIConfig.FAVORITE_PRODUCTS_ROUTES_MAPPER
)

favorite_products_router = APIRouter(
    prefix=APIConfig.FAVORITE_PRODUCTS_ROUTE_PREFIX,
    tags=favorite_products_routes_mapper.tags,
    dependencies=[Depends(JWTBearerAuth())]
)


@cbv(favorite_products_router)
class ServiceFavoriteProductsAPIRouter:

    @favorite_products_router.get(
        favorite_products_routes_mapper.get_all,
        response_model=ServiceProviderResponse
    )
    async def get_favorite_products_list(
        self,
        client_id: int
    ):
        try:
            products = await FavoriteProductsRepository().get_favorite_products_list(client_id)
            response = FavoriteProductsListView(
                count=len(products),
                client_id=client_id,
                favorite_products=products
            )
            logger.info("Ouieh! Got products data successfully!")
            return await ServiceProviderResponse.from_response(response=response.model_dump())
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @favorite_products_router.get(
        favorite_products_routes_mapper.get_by,
        response_model=ServiceProviderResponse
    )
    async def get_favorite_product_from_list(
        self,
        client_id: int,
        product_id: uuid_pkg.UUID
    ):
        try:
            response = await FavoriteProductsRepository().get_favorite_product_from_list(
                client_id=client_id,
                product_id=product_id
            )
            logger.info("Ouieh! Got product data successfully!")
            return await ServiceProviderResponse.from_response(response=response)
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @favorite_products_router.post(
        favorite_products_routes_mapper.create,
        response_model=ServiceProviderResponse
    )
    async def include_favorite_product_to_list(
        self,
        product_register: FavoriteProductsRegister
    ):
        try:
            favorite_product = await FavoriteProductsRepository().include_to_list(product_register)
            response = FavoriteProductView(
                message="Product included into favorite products list successfully",
                client_id=product_register.client_id,
                product=favorite_product
            )
            logger.info("Ouieh! Product included into favorite products list successfully!")
            return await ServiceProviderResponse.from_response(
                response=response.model_dump(),
                status_code=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @favorite_products_router.delete(
        favorite_products_routes_mapper.delete['from-list'],
        response_model=ServiceProviderResponse
    )
    async def remove_favorite_product_from_list(
        self,
        client_id: int,
        product_id: uuid_pkg.UUID
    ):
        try:
            await FavoriteProductsRepository().remove_favorite_product_from_list(
                client_id=client_id,
                product_id=product_id
            )
            logger.info("Ouieh! Product deleted successfully!")
            return await ServiceProviderResponse.from_response(
                response={'message': "Product deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @favorite_products_router.delete(
        favorite_products_routes_mapper.delete['list'],
        response_model=ServiceProviderResponse
    )
    async def delete_favorite_products_list(
        self,
        client_id: int
    ):
        try:
            await FavoriteProductsRepository().delete_favorite_products_list(client_id=client_id)
            logger.info("Ouieh! Product deleted successfully!")
            return await ServiceProviderResponse.from_response(
                response={'message': "Favorite products list deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)
