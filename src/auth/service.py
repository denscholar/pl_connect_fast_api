from typing import List
from sqlmodel import select, desc
from fastapi import status, HTTPException
from src.auth.utils import check_referral_code_exists, generate_referral_code
from .schemas import CreateUser
from .models import User
from src.db.main import engine
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import uuid
from .security import hash_password, verify_password


class UserService:
    """
    Docstring for UserService
    """

    async def get_user_by_phone(self, phone_number: str, session: AsyncSession):
        # GET USER BY PHONE AND RETURN THE USER OBJECT IF EXISTS ELSE NONE
        statement = select(User).where(User.phone_number == phone_number)
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None

    async def user_exists(self, phone_number: str, session: AsyncSession) -> bool:
        # CHECK IF USER EXISTS BY PHONE NUMBER
        user = await self.get_user_by_phone(phone_number, session)
        return True if user is not None else False

    async def create_user(self, user_data: CreateUser, session: AsyncSession):
        # CREATE A NEW USER AND RETURN THE USER OBJECT
        user_data_dict = user_data.model_dump()

        # Remove confirm_password before creating User
        user_data_dict.pop("confirm_password", None)

        # Hash the password
        hashed_pw = hash_password(user_data_dict["password"])

        # don’t store plain password
        user_data_dict.pop("password")

        user_data_dict["hashed_password"] = hashed_pw

        # extract the referral_code check for validity
        referral_code = user_data_dict["referral_code"]
        referral_code_exist = await check_referral_code_exists(
            session=session, code=referral_code
        )

        if referral_code_exist is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid referral code provided.",
            )

        # generate referal code
        generate_user_referral_code = await generate_referral_code(session)
        user_data_dict["referral_code"] = generate_user_referral_code

        # also set who referred them (if applicable)
        user_data_dict["referred_by"] = (
            referral_code_exist.uid if referral_code else None
        )

        # change is_active and is_verified to True
        user_data_dict["is_active"] = True
        user_data_dict["is_verified"] = True

        new_user = User(**user_data_dict)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
