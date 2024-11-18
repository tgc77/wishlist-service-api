from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import EmailStr


class ClientBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=50)
    name: str = Field(nullable=False, max_length=50)


class ClientModel(ClientBase, table=True):
    __tablename__ = "tb_api_client"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)

    def __bool__(self):
        return bool(all([self.email, self.name]))
