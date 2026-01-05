from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List

from src.auth.models import User
from .schemas import (
    CreateUser,
    CustomRegisterResponse,
    UserLoginRequest,
    UserModelResponse,
)
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
import uuid
from .security import create_access_token, verify_password, decode_access_token
from datetime import timedelta


auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.post(
    "/register",
    response_model=CustomRegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_account(
    user_data: CreateUser, session: AsyncSession = Depends(get_session)
):
    # Here you would call your UserService to create the user
    phone_number = user_data.phone_number
    user_exists = await user_service.user_exists(phone_number, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this phone number already exists.",
        )

    new_user = await user_service.create_user(user_data, session)

    referred_by_phone_number = None

    if new_user.referred_by:
        referrer = await session.get(User, new_user.referred_by)
        referred_by_phone_number = referrer.phone_number

    return {
        "message": "created successfully",
        "uid": str(new_user.uid),
        "phone_number": new_user.phone_number,
        "referral_code": new_user.referral_code,
        "referred_by_phone_number": referred_by_phone_number,
    }


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user_login_data: UserLoginRequest, session: AsyncSession = Depends(get_session)
):
    # extract the phone number and password
    phone_number = user_login_data.phone_number
    password = user_login_data.password

    # check if user exists
    user = await user_service.get_user_by_phone(phone_number, session)

    if user is not None:
        if verify_password(password, user.hashed_password):
            access_token = create_access_token(
                user_data={"phone_number": user.phone_number, "uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"phone_number": user.phone_number, "uid": str(user.uid)},
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "uid": str(user.uid),
                        "phone_number": user.phone_number,
                    },
                }
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password.",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid phone number",
    )

   