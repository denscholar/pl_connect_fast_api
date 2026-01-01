from fastapi import FastAPI, Header, status
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
async def get_root():
    return {
        "detail": "Welcome to fast API",
    }


# mixing both path parameters and query parameters implementation
@app.get("/user/{age}")
async def get_name(name: str, age: int) -> dict:
    return {
        "message": f"Hello {name} I am {age} years old",
    }


# how to make query params and path parameters optional with default value
@app.get("/greet")
async def greet_name(age: Optional[int] = 25, name: Optional[str] = "User"):
    return {
        "message": f"Good day {name} I am {age} years old",
    }


# This is used to validate what goes into the server
class BookCreateModel(BaseModel):
    title: str
    author: str


# Request body - post request
@app.post("/create_book")
async def create_book(book_data: BookCreateModel):
    return {
        "title": book_data.title,
        "autor": book_data.author,
    }


# how to access the request headers
@app.get("/get_headers", status_code=status.HTTP_200_OK)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None),
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers
