
from typing import Optional

import jwt
from fastapi import HTTPException, status, Request
from jwt.exceptions import InvalidTokenError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.core.settings import APIConfig


class JWTBearerAuth(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearerAuth, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearerAuth, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            token = credentials.credentials
            if not self.validate_token(token):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )
            return token
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization code.")

    def validate_token(self, token: str) -> bool:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            decoded_token = jwt.decode(
                token, APIConfig.SECRET_KEY, algorithms=[
                    APIConfig.HASH_ALGORITHM]
            )
            username: str = decoded_token.get("sub")
            if username is None:
                raise credentials_exception

            return True
        except InvalidTokenError:
            raise credentials_exception
