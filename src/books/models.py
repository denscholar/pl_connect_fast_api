# here will have the database model for books
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel, Field
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
import uuid


class Book(SQLModel, table=True):
    __tablename__ = "books"
    # uid: str = Field(default=None, primary_key=True, sa_column=Column(String, default=lambda: str(uuid.uuid4()))) => supports any database
    uid: str = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
        ),
    )  # supports only postgresql database
    title: str = Field(sa_column=Column(String, index=True, nullable=False))
    author: str = Field(sa_column=Column(String, index=True, nullable=False))
    publisher: str = Field(sa_column=Column(String, index=True, nullable=False))
    published_date: str = Field(sa_column=Column(String, nullable=False))
    page_count: int = Field(sa_column=Column(Integer, nullable=False))
    language: str = Field(sa_column=Column(String, nullable=False))
    created_at: datetime = Field(
        Column(pg.TIMESTAMP(timezone=True), default=datetime.now, nullable=False)
    )
    updated_at: datetime = Field(
        Column(pg.TIMESTAMP(timezone=True), default=datetime.now, nullable=True)
    )


    def __repr__(self):
        return f"Book(uid={self.uid}, title={self.title}, author={self.author}, publisher={self.publisher}, published_date={self.published_date}, page_count={self.page_count}, language={self.language})"

