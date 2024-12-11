from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm

from api.core.settings import APIConfig
from api.core.entities.token import Token
from api.core.security.user_authenticator import UserAuthenticator
from api.core.database import AsyncSession, get_async_session

auth_router = APIRouter(
    tags=["Authentication"]
)


@auth_router.post("/auth")
async def login_for_access_token(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    user_authenticator = UserAuthenticator(session)
    user = await user_authenticator.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=APIConfig.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = user_authenticator.create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires
    )
    request.app.state.current_user = user.username
    return Token(access_token=access_token, token_type="bearer")
