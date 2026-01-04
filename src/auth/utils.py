import random
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlmodel import select
from typing import Optional
from .models import User

async def generate_referral_code(session: Session) -> int:
    """
    Generate a unique 6-digit referral code.
    Retries automatically if a duplicate is hit.
    """
    while True:
        code = random.randint(100000, 999999)
        # Check if code already exists
        result = await session.exec(select(User).where(User.referral_code == code))
        exists = result.first()
        if not exists:
            return code
        

async def check_referral_code_exists(session: Session, code: int) -> Optional[User]:
    """
    Check if a referral code already exists in the database.
    """
    result = await session.exec(select(User).where(User.referral_code == code))
    return result.first()



# def create_user(session: Session, phone_number: str, hashed_password: str, **kwargs) -> User:
#     """
#     Safely create a new user with a unique referral code.
#     Retries if a race condition causes duplicate referral_code.
#     """
#     while True:
#         try:
#             new_user = User(
#                 phone_number=phone_number,
#                 hashed_password=hashed_password,
#                 referral_code=generate_referral_code(session),
#                 **kwargs
#             )
#             session.add(new_user)
#             session.commit()
#             return new_user
#         except IntegrityError:
#             # Rollback and retry if duplicate referral_code was inserted
#             session.rollback()
#             continue



