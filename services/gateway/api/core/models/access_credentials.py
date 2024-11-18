from typing import Optional
from sqlmodel import Field, SQLModel, Column, ForeignKey, String
from pydantic import EmailStr

from api.core.models.client import ClientModel


class AccessCredentialsBase(SQLModel):
    client_id: int = Field(index=True, foreign_key=f"{ClientModel.__tablename__}.id")
    email: EmailStr = Field(
        sa_column=Column(
            "email",
            String(50),
            ForeignKey(
                f"{ClientModel.__tablename__}.email",
                onupdate="CASCADE", ondelete="CASCADE"
            ),
            index=True
        )
    )
    username: str = Field(unique=True, nullable=False, max_length=30, index=True)
    active: bool = Field(default=True)
    scope: str = Field(default=None)

    def __bool__(self):
        return bool(all([self.client_id, self.username]))


class AccessCredentialsModel(AccessCredentialsBase, table=True):
    __tablename__ = "tb_api_access_credentials"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str = Field()


class AccessCredentialsData(AccessCredentialsBase):
    pass
