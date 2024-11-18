import uuid as uuid_pkg
from decimal import Decimal

from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    title: str = Field(default=None, nullable=False, max_length=50)
    brand: str = Field(default=None, nullable=False, max_length=50)
    price: Decimal = Field(default=0, max_digits=6, decimal_places=2)
    image: str = Field(default=None, max_length=200)

    def __bool__(self):
        return bool(all([self.title, self.price]))


class ProductModel(ProductBase, table=True):
    __tablename__ = "tb_api_product"

    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True
    )
