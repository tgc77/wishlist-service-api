
from typing import List, Optional
from pydantic import (
    EmailStr,
    BaseModel as PydanticBaseModel,
    Field
)


class ClientBase(PydanticBaseModel):
    email: EmailStr = Field(
        default=None, unique=True,
        index=True, max_length=50
    )
    name: str = Field(default=None, nullable=False, max_length=50)

    def __bool__(self):
        return bool(all([self.email, self.name]))


class ClientRegister(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientEntity(ClientBase):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    class Config:
        from_attributes = True
        validate_default = True


class ClientsView(PydanticBaseModel):
    clients: List[ClientEntity]
    count: int
