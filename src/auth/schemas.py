from typing import Optional
from pydantic import BaseModel, Field, model_validator
from fastapi import status, HTTPException

import uuid
from datetime import datetime, date


class CreateUser(BaseModel):
    phone_number: str = Field()
    referral_code: int
    nickname: str = Field(max_length=20)
    password: str = Field(min_length=8, max_length=64)
    confirm_password: str = Field(min_length=8, max_length=64)

    # Validate confirm_password against password
    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise HTTPException(
                detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
            )
        return self


class UserModelResponse(BaseModel):
    uid: uuid.UUID
    phone_number: str
    referral_code: int
    nickname: str
    is_active: bool
    is_verified: bool
    full_name: Optional[str]
    hashed_password: str = Field(exclude=True)
    email: Optional[str]
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CustomRegisterResponse(BaseModel):
    message: str
    uid: uuid.UUID
    phone_number: str
    referral_code: int
    referred_by_phone_number: Optional[str] = None


class UserLoginRequest(BaseModel):
    phone_number: str
    password: str


class UserLoginResponse(BaseModel):
    message: str
    uid: uuid.UUID
    phone_number: str
    referral_code: int
    referred_by_phone_number: Optional[str] = None