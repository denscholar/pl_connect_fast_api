from pydantic import BaseModel
import uuid
from datetime import datetime, date


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S"),
            date: lambda v: v.strftime("%d-%m-%Y")
        }



class CreateBook(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    published_date: date
    language: str

class UpdateBook(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
