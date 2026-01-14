import bcrypt
from datetime import timedelta, datetime, timezone
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
import jwt
from src.config import Config
import uuid


ACCESS_TOKEN_EXPIRIY_SECONDS = 3600  # 1 hour
REFRESH_TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 7

# HASH PASSWORD - Bcrypt
def hash_password(password: str) -> str:
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


# VERIFY PASSWORD - Bcrypt
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


# CREATE JWT ACCESS TOKEN - Encoding
def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
) -> str:
    payload = {"user": user_data}

    if expiry is None:
        expiry = timedelta(seconds=REFRESH_TOKEN_EXPIRY_SECONDS if refresh else ACCESS_TOKEN_EXPIRIY_SECONDS)

    payload["exp"] = datetime.now(timezone.utc) + expiry

    # unique identifier for the token
    payload["jti"] = str(uuid.uuid4())

    # optional refresh token indicator
    payload["refresh"] = refresh

    token = jwt.encode(
        payload,
        key=Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM,
    )
    return token


# DECODE JWT ACCESS TOKEN - Decoding
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# BEARER TOKEN AUTHENTICATION IMPLEMENTATION
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(TokenBearer, self).__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            
            token_data = decode_access_token(credentials.credentials)
            self.verify_token_data(token_data)
            return token_data

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization token",
            )

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please overide this method in child class")



class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh", False) and token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide an access token",
                headers={"WWW-Authenticate": "Bearer"},
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh", False) and token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide a refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    @staticmethod
    def decode_refresh_token(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                key=Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM],
                options={"verify_exp": False}
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

