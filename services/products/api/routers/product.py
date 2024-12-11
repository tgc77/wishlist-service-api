
import uuid as uuid_pkg
from typing import Optional
from fastapi import Depends, status, APIRouter
from fastapi_utils.cbv import cbv

from api.core.entities.product import (
    ProductRegister,
    ProductUpdate,
    FavoriteProductsView,
    ProductsMetadata,
    ProductReview
)
from api.core.security.user_authenticator import JWTBearerAuth
from api.core.database import AsyncSession, get_async_session
from api.core.logger import logger
from api.core.repositories.product import ProductRepository
from api.core.response import ServiceProviderResponse
from api.core.settings import APIConfig
from .route_mapper import ServiceApiRouteMapper

products_routes_mapper = ServiceApiRouteMapper.load_from_apiconfig(APIConfig.PRODUCTS_ROUTES_MAPPER)

products_router = APIRouter(
    prefix=APIConfig.PRODUCTS_ROUTE_PREFIX,
    tags=products_routes_mapper.tags,
    dependencies=[Depends(JWTBearerAuth())]
)


@cbv(products_router)
class ServiceProductsAPIRouter:
    session: AsyncSession = Depends(get_async_session)

    @products_router.get(
        products_routes_mapper.get_all,
        response_model=ServiceProviderResponse
    )
    async def get_products(
        self,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ):
        try:
            products = await ProductRepository(self.session).get_all_by_filters(
                limit=limit,
                offset=offset
            )
            products_metada = ProductsMetadata(
                page=dict(
                    limit=limit,
                    offset=offset,
                    count=len(products)
                )
            )
            favorite_producst_view = FavoriteProductsView(
                meta=products_metada,
                results=products
            )
            logger.info("Ouieh! Got products data successfully!")
            return await ServiceProviderResponse.from_response(response=favorite_producst_view)
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @products_router.get(
        products_routes_mapper.get_by,
        response_model=ServiceProviderResponse
    )
    async def get_product_by_id(
        self,
        id: uuid_pkg.UUID
    ):
        try:
            product = await ProductRepository(self.session).get_by_id(id=id)
            link_product_review = "/".join([
                APIConfig.API_GATEWAY_SERVICE_URL,
                'products',
                products_routes_mapper.review.format(id=product.id)
            ])
            product_json = product.model_dump(exclude={'id', 'price'})
            product_review = ProductReview(
                **product_json
            )
            product_review.link_review = link_product_review
            product_review.id = str(product.id)
            product_review.price = float(product.price)
            response = product_review.model_dump()
            logger.info("Ouieh! Got product data successfully!")
            return await ServiceProviderResponse.from_response(response=response)
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @products_router.get(
        products_routes_mapper.review,
        response_model=ServiceProviderResponse
    )
    async def get_product_review(
        self,
        id: uuid_pkg.UUID
    ):
        try:
            product_review_path = (
                "Hi there! I'm supose to be a html template to show product review. "
                f"Actually I've got a product_id: {id}, so what should I do?"
            )
            return await ServiceProviderResponse.from_response(response=product_review_path)
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @products_router.post(
        products_routes_mapper.create,
        response_model=ServiceProviderResponse
    )
    async def register_product(
        self,
        product_register: ProductRegister
    ):
        try:
            new_product = await ProductRepository(self.session).register(product_register)
            logger.info("Ouieh! Product register successfully!")
            return await ServiceProviderResponse.from_response(
                response={
                    'message': "Product register successfully!",
                    'product': new_product
                },
                status_code=status.HTTP_201_CREATED
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @products_router.patch(
        products_routes_mapper.update,
        response_model=ServiceProviderResponse
    )
    async def update_product(
        self,
        id: uuid_pkg.UUID,
        product_update: ProductUpdate
    ):
        try:
            product = await ProductRepository(self.session).update(id=id, product_update=product_update)
            logger.info("Ouieh! Product updated successfully!")
            return await ServiceProviderResponse.from_response(
                response={
                    'message': "Product updated successfully!",
                    'product': product
                }
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)

    @products_router.delete(
        products_routes_mapper.delete,
        response_model=ServiceProviderResponse
    )
    async def delete_product(
        self,
        id: uuid_pkg.UUID
    ):
        try:
            await ProductRepository(self.session).delete(id=id)
            logger.info("Ouieh! Product deleted successfully!")
            return await ServiceProviderResponse.from_response(
                response={'message': "Product deleted successfully!"}
            )
        except Exception as ex:
            logger.error(f"Oops! Got some trouble here: {ex}")
            return await ServiceProviderResponse.from_exception(exception=ex)
