
import uuid as uuid_pkg
from typing import Dict, List, Optional
from pydantic import (
    BaseModel as PydanticBaseModel,
    Field
)


class FavoriteProductsBase(PydanticBaseModel):
    product_id: uuid_pkg.UUID
    favorite_products_list_id: Optional[int] = Field(default=None)


class FavoriteProductsRegister(FavoriteProductsBase):
    client_id: int


class FavoriteProductsRemove(FavoriteProductsBase):
    client_id: int


class FavoriteProductsEntity(FavoriteProductsBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

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


class FavoriteProductsListView(PydanticBaseModel):
    count: int
    client_id: int
    favorite_products: List[Dict]


class FavoriteProductView(PydanticBaseModel):
    message: str
    client_id: int
    product: Dict
