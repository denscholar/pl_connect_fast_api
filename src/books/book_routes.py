from fastapi import APIRouter, status, HTTPException
from typing import List
from .schimas import Book, UpdateBook
from .book_data import books

router = APIRouter()


@router.get("/", response_model=List[Book])
async def get_all_books():
    return books


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@router.get("/{book_id}")
async def get_a_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.patch("/{book_id}")
async def updating_a_book(book_id: int, book_update: UpdateBook) -> dict:
    for book in books:
        if book["id"] == book_id:
            # Update only provided fields
            book["title"] = book_update.title
            book["author"] = book_update.author
            book["publisher"] = book_update.publisher
            book["page_count"] = book_update.page_count
            book["language"] = book_update.language

            return book
    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book[id] == book_id:
            books.remove(book)
            return {}

    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


# Note: that doing this isnt just enough. We still need to input it in our app to be able to use it.
