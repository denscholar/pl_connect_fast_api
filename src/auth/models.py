from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from sqlalchemy.dialects.postgresql import TIMESTAMP
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Column, String, Integer, Boolean
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
    referred_by: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="users.uid",  # self-referencing FK
        nullable=True
    )
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    full_name: Optional[str] = None
    email: Optional[str] = Field(sa_column=Column(String, unique=True, index=True))
    is_admin: bool = Field(sa_column=Column(Boolean, default=False, nullable=False))
    hashed_password: str = Field(sa_column=Column(String, nullable=False), exclude=True)
    nickname: str = Field(sa_column=Column(String, nullable=False), max_length=20)
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False), default_factory=datetime.now

    )
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), default=datetime.now, nullable=False)
    )

    # Relationships
    referrer: Optional["User"] = Relationship(back_populates="referrals", sa_relationship_kwargs={"remote_side": "User.uid"})
    referrals: list["User"] = Relationship(back_populates="referrer")


    def __repr__(self):
        return f"User(uid={self.uid}, phone_number={self.phone_number}, referral_code={self.referral_code})"
