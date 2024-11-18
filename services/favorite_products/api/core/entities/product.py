
from decimal import Decimal
import uuid as uuid_pkg
from typing import List, Optional
from pydantic import (
    BaseModel as PydanticBaseModel,
    Field
)


class ProductBase(PydanticBaseModel):
    title: str = Field(default=None, nullable=False, max_length=50)
    brand: str = Field(default=None, nullable=False, max_length=50)
    price: Decimal = Field(default=0, max_digits=6, decimal_places=2)
    image: str = Field(default=None, max_length=200)

    def __bool__(self):
        return bool(all([self.title, self.price]))


class ProductRegister(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductEntity(ProductBase):
    id: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )

    class Config:
        from_attributes = True
        validate_default = True


class ProductsView(PydanticBaseModel):
    products: List[ProductEntity]
    count: int
