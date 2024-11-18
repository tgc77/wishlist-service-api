from typing import Optional
from sqlmodel import Field, SQLModel, UniqueConstraint
import uuid as uuid_pkg

from api.core.models.product import ProductModel
from api.core.models.client import ClientModel


class FavoriteProductsListBase(SQLModel):
    client_id: int = Field(
        index=True,
        foreign_key=f"{ClientModel.__tablename__}.id",
        ondelete="CASCADE"
    )


class FavoriteProductsListModel(FavoriteProductsListBase, table=True):
    __tablename__ = "tb_api_client_favorite_products_list"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    def __bool__(self):
        return bool(all([self.client_id]))


class FavoriteProductsBase(SQLModel):
    favorite_products_list_id: int = Field(
        index=True,
        foreign_key=f"{FavoriteProductsListModel.__tablename__}.id",
        ondelete="CASCADE"
    )
    product_id: uuid_pkg.UUID = Field(
        index=True,
        foreign_key=f"{ProductModel.__tablename__}.id",
        ondelete="CASCADE"
    )


class FavoriteProductsModel(FavoriteProductsBase, table=True):
    __tablename__ = "tb_api_client_favorite_products"
    __table_args__ = (
        UniqueConstraint("favorite_products_list_id", "product_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    def __bool__(self):
        return bool(all([self.favorite_products_list_id, self.product_id]))
