from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import TIMESTAMP
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, String, Integer
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    )
    phone_number: str = Field(
        sa_column=Column(String, unique=True, index=True, nullable=False)
    )
    referral_code: int = Field(
        sa_column=Column(Integer, unique=True, index=True, nullable=False)
    )
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    full_name: Optional[str] = None
    email: Optional[str] = Field(sa_column=Column(String, unique=True, index=True))
    nickname: str = Field(sa_column=Column(String, nullable=False), max_length=20)
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False)
    )

    def __repr__(self):
        return f"User(uid={self.uid}, phone_number={self.phone_number}, referral_code={self.referral_code})"
