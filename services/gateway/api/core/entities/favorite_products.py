
import uuid as uuid_pkg
from typing import Dict, List, Optional
from pydantic import (
    BaseModel as PydanticBaseModel,
    Field
)

from api.core.entities.product import ProductEntity


class FavoriteProductsBase(PydanticBaseModel):
    product_id: uuid_pkg.UUID


class FavoriteProductsRegister(FavoriteProductsBase):
    client_id: int


class FavoriteProductsEntity(FavoriteProductsBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    favorite_products_list_id: Optional[int] = Field(default=None)

    class Config:
        from_attributes = True
        validate_default = True


class FavoriteProductsListBase(PydanticBaseModel):
    client_id: Optional[int] = Field(default=None)


class FavoriteProductsListEntity(FavoriteProductsListBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    class Config:
        from_attributes = True
        validate_default = True


class FavoriteProductsView:
    meta: Dict[str, Dict[str, int]] = dict(
        page=dict(
            limit=20,
            offset=2,
            count=0
        )
    )
    results: List[ProductEntity] = []


class FavoriteProductsListView:
    favorite_products: List[FavoriteProductsView]
    count: int
