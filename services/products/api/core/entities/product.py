
from decimal import Decimal
from typing_extensions import TypedDict
import uuid as uuid_pkg
from typing import Dict, List, Optional
from pydantic import (
    BaseModel as PydanticBaseModel,
    Field
)


class ProductBase(PydanticBaseModel):
    title: Optional[str] = Field(default=None, nullable=False, max_length=50)
    brand: Optional[str] = Field(default=None, nullable=False, max_length=50)
    image: Optional[str] = Field(default=None, max_length=200)
    price: Optional[Decimal] = Field(default=0, max_digits=6, decimal_places=2)

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


class ProductsMetadata(TypedDict, total=False):
    page: Dict[str, int] = dict(
        limit=20,
        offset=0,
        count=0
    )


class FavoriteProductsView(TypedDict):
    meta: Dict[str, ProductsMetadata]
    results: List[ProductEntity] = []


class ProductReview(PydanticBaseModel):
    id: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    brand: Optional[str] = Field(default=None)
    image: Optional[str] = Field(default=None)
    price: Optional[float] = Field(default=0)
    link_review: Optional[str] = Field(default=None)
