import json

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from api.core.settings import APIConfig


password_crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth",
    scopes=json.loads(APIConfig.ACCESS_AUTHENTICATION_SCOPES)
)
