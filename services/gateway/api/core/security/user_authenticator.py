from dataclasses import dataclass
from typing import Annotated, Dict
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import SecurityScopes
from jwt.exceptions import InvalidTokenError

from api.core.entities.token import TokenData
from api.core.database import AsyncSession, get_async_session
from api.core.entities.access_credentials import AccessCredentialsEntity
from api.core.repositories.access_credentials import AccessCredentialsRepository
from api.core.repositories.client import ClientRepository
from api.core.settings import APIConfig
from api.core.logger import logger
from api.core.error_handlers import UserAccessForbidden
from api.core.security.password_crypt import (
    password_crypt_context,
    oauth2_scheme
)


class CredentialsException:

    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Could not validate credentials"
        self.auth_header_key = 'WWW-Authenticate'
        self.auth_header_bearer = "Bearer"
        self.auth_header_bearer_scopes = "Bearer scopes={sec_scope}"
        self.security_scope: str
        self.auth_header = {
            self.auth_header_key: self.auth_header_bearer
        }

    def set_authentication_scope(self, scope: str):
        self.security_scope = scope
        self.auth_header_bearer_scopes.format(sec_scope=scope)
        self.auth_header = {
            self.auth_header_key: self.auth_header_bearer_scopes
        }

    def raise_it(self, detail: str = None):
        raise HTTPException(
            status_code=self.status_code,
            detail=detail or self.detail,
            headers=self.auth_header,
        )


@dataclass
class UserAuthenticator:
    session: AsyncSession = None

    def verify_password(self, plain_password: str, hashed_password: str):
        return password_crypt_context.verify(plain_password, hashed_password)

    def generate_hashed_password(self, password):
        return password_crypt_context.hash(password)

    async def register_credentials(self, access_credentials: AccessCredentialsEntity):
        try:
            hashed_password = self.generate_hashed_password(access_credentials.password)
            access_credentials.password = hashed_password
            client_data = await ClientRepository(self.session).get_by_email(access_credentials.email)
            new_access_credentials = AccessCredentialsEntity(**access_credentials.model_dump())
            new_access_credentials.client_id = client_data.id
            await AccessCredentialsRepository(self.session).register(
                access_credentials_create=AccessCredentialsEntity.model_validate(new_access_credentials)
            )
            logger.info("Ouieh! User credentials registered successfully")
        except Exception as ex:
            logger.error(f"Oops! Could not register access credentials for this user: {ex}")
            raise ex

    async def validate_user_access_credentials(self, username: str) -> AccessCredentialsEntity:
        try:
            access_credentials = await AccessCredentialsRepository(session=self.session).get_by_username(username)
            return access_credentials
        except Exception as ex:
            logger.error(f"Oops!{ex}")
            return None

    async def authenticate_user(self, username: str, password: str):
        try:
            user = await self.validate_user_access_credentials(username)
            if not user:
                return False
            if not self.verify_password(password, user.password):
                return False
            return user
        except Exception as ex:
            logger.error(f"Oops! Could not authenticate user: {ex}")
            return False

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, APIConfig.SECRET_KEY, algorithm=APIConfig.HASH_ALGORITHM
        )
        return encoded_jwt


async def validate_access_credentials(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_async_session)
) -> AccessCredentialsEntity:
    credentials_exception = CredentialsException()
    if security_scopes.scopes:
        credentials_exception.set_authentication_scope(security_scopes.scope_str)
    try:
        decoded_token = jwt.decode(
            token, APIConfig.SECRET_KEY, algorithms=[APIConfig.HASH_ALGORITHM]
        )
        username: str = decoded_token.get("sub")
        if username is None:
            credentials_exception.raise_it()

        token_scopes = decoded_token.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except InvalidTokenError:
        credentials_exception.raise_it()

    user = await UserAuthenticator(session).validate_user_access_credentials(username=token_data.username)
    if user is None:
        credentials_exception.raise_it()

    if not user.active:
        raise UserAccessForbidden(detail="Inactive user")

    for scope in token_data.scopes:
        if scope not in security_scopes.scopes:
            credentials_exception.raise_it(detail="Not enough permissions")

    user.token = token
    return user


async def require_access_scope_as_admin(
    access_credentials: Annotated[
        AccessCredentialsEntity, Security(
            validate_access_credentials, scopes=["admin"]
        )
    ]
):
    return {"Authorization": f"Bearer {access_credentials.token}"}


async def require_access_scope_as_client(
    access_credentials: Annotated[
        AccessCredentialsEntity, Security(
            validate_access_credentials, scopes=["client"]
        )
    ]
):
    return {"Authorization": f"Bearer {access_credentials.token}"}


async def require_access_scope_as_admin_or_client(
    access_credentials: Annotated[
        AccessCredentialsEntity, Security(
            validate_access_credentials, scopes=["admin", "client"]
        )
    ]
):
    return {"Authorization": f"Bearer {access_credentials.token}"}


AdminAccessAuthorizationHeader = Annotated[Dict, Depends(require_access_scope_as_admin)]
ClientAccessAuthorizationHeader = Annotated[Dict, Depends(require_access_scope_as_admin_or_client)]


async def validate_access_credetials_as_admin(
    access_credentials: Annotated[
        AccessCredentialsEntity, Security(
            validate_access_credentials, scopes=["admin"]
        )
    ]
):
    return access_credentials
