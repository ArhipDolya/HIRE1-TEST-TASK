from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.settings.config import get_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config = get_config()


def create_token(data: dict, expires_delta: timedelta):
    data_to_encode = data.copy()
    expire = datetime.now() + expires_delta
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


def create_access_token(data: dict):
    return create_token(data, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: dict):
    return create_token(data, timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS))


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: Whether the plain password matches the hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def decode_token(token: str):
    return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
