import bcrypt
from datetime import timedelta, datetime, timezone
from fastapi.security import HTTPBearer 
from fastapi import Request, HTTPException, status
import jwt
from src.config import Config
import uuid


ACCESS_TOKEN_EXPIRIY_SECONDS = 3600  # 1 hour

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
    payload = {}
    payload["user"] = user_data

    payload["exp"] = (
        datetime.now(timezone.utc) + expiry
        if expiry is not None
        else datetime.now(timezone.utc)
        + timedelta(seconds=ACCESS_TOKEN_EXPIRIY_SECONDS)
    )
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
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")



# BEARER TOKEN AUTHENTICATION IMPLEMENTATION
class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AccessTokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(AccessTokenBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            try:
                token_data = decode_access_token(credentials.credentials)
                return token_data
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=str(e),
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization token",
            )