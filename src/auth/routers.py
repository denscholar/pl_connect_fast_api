from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from src.auth.models import User
from .schemas import CreateUser, CustomRegisterResponse, UserModelResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
import uuid

auth_router = APIRouter()
user_service = UserService()


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

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_user(user_data: CreateUser, session: AsyncSession = Depends(get_session)):
    pass


    # return {
    #     "message": "created successfully",
    #     "uid": str(new_user.uid), # convert UUID to string if needed
    #     "phone_number": new_user.phone_number,
    #     "referral_code": new_user.referral_code,
    #     "referred_by_phone_number": new_user.referrer.phone_number if new_user.referrer else None

    # }
