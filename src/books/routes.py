from fastapi import APIRouter, status, HTTPException, Depends
from typing import List

from src.books.service import BookService
from .schemas import Book, CreateBook, UpdateBook
from .book_data import books
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
import uuid
from src.auth.dependencies import AccessTokenBearer

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()




@router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session), user_detail=Depends(access_token_bearer)):
    books = await book_service.get_all_books(session)
    return books


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: CreateBook, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    # new_book = book_data.model_dump()
    # books.append(new_book)
    return new_book


@router.get("/{book_uid}", response_model=Book)
async def get_a_book(book_uid: uuid.UUID, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    # for book in books:
    #     if book["uid"] == book_uid:
    #         return book
    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.patch("/{book_uid}")
async def updating_a_book(
    book_uid: uuid.UUID, book_update: UpdateBook, session: AsyncSession = Depends(get_session)
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update, session)
    if updated_book:
        return updated_book
    
    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_uid: uuid.UUID, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)
    if book_to_delete:
        return {}
    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )

