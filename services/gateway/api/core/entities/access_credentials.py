
from typing import Optional
from pydantic import (
    BaseModel as PydanticBaseModel,
    Field,
    EmailStr
)


class AccessCredentialsBase(PydanticBaseModel):
    email: Optional[EmailStr] = Field(unique=True, nullable=False, max_length=50)
    username: Optional[str] = Field(default=None, nullable=False, max_length=30)
    active: Optional[bool] = Field(default=True)


class AccessCredentialsRegister(AccessCredentialsBase):
    password: Optional[str] = Field(default=None, min_length=6)
    scope: Optional[str] = Field(default='client')


class AccessCredentialsEntity(AccessCredentialsBase):
    id: Optional[int] = Field(default=None)
    client_id: Optional[int] = Field(default=None)
    password: Optional[str] = Field(default=None, min_length=6)
    token: Optional[str] = Field(default=None)
    scope: Optional[str] = Field(default='client')

    def __bool__(self):
        return bool(all([self.client_id, self.username]))

    class Config:
        from_attributes = True
        validate_default = True
