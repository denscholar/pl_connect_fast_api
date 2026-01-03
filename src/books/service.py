from typing import List
from sqlmodel import select, desc
from src.books.schemas import CreateBook, UpdateBook
from src.db.main import engine
from datetime import datetime
from .models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
import uuid


class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        books = result.all()
        return books

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data: CreateBook, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(
            uid=uuid.uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            **book_data_dict
        )
        statement = new_book
        session.add(statement)
        await session.commit()
        # await session.refresh(statement)
        return new_book

    async def update_book(
        self, uid: str, update_data: UpdateBook, session: AsyncSession
    ):
        book_to_update = self.get_book(uid, session)
        if not book_to_update:
            return None

        update_data_dict = update_data.model_dump()
        for key, value in update_data_dict.items():
            setattr(book_to_update, key, value)

        await session.commit()
        await session.refresh(book_to_update)
        return book_to_update

    async def delete_book(self, uid: str, session: AsyncSession) -> None:
        book_to_delete = self.get_book(uid, session)
        if book_to_delete:
            await session.delete(book_to_delete)
            await session.commit()
        return None
