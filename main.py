from fastapi import FastAPI, Header, status, HTTPException
from typing import Optional, List
from pydantic import BaseModel


app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "publisher": "Prentice Hall",
        "published_date": "2008-08-01",
        "page_count": 464,
        "language": "en",
    },
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "Andrew Hunt, David Thomas",
        "publisher": "Addison-Wesley",
        "published_date": "1999-10-30",
        "page_count": 352,
        "language": "en",
    },
    {
        "id": 3,
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein",
        "publisher": "MIT Press",
        "published_date": "2009-07-31",
        "page_count": 1312,
        "language": "en",
    },
    {
        "id": 4,
        "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
        "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
        "publisher": "Addison-Wesley",
        "published_date": "1994-10-21",
        "page_count": 395,
        "language": "en",
    },
    {
        "id": 5,
        "title": "Deep Learning",
        "author": "Ian Goodfellow, Yoshua Bengio, Aaron Courville",
        "publisher": "MIT Press",
        "published_date": "2016-11-18",
        "page_count": 800,
        "language": "en",
    },
]


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class UpdateBook(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


@app.get("/book/{book_id}")
async def get_a_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )


@app.patch("/book/{book_id}")
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


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int):
    for book in books:
        if book[id] == book_id:
            books.remove(book)
            return {}

    raise HTTPException(
        detail="book not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )
