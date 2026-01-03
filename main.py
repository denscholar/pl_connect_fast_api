from fastapi import FastAPI, Header, status, HTTPException
from typing import Optional, List
from .src.books.book_data import books
from .src.books.schemas import Book, UpdateBook


app = FastAPI()


