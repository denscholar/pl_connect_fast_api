from fastapi import FastAPI
from src.books.book_routes import router

version = "v1"

app = FastAPI(
    title='PL Connect API endpoints',
    description="This endpoints will be used for the development of PL connect mobile application for people living with HIV/AIDS",
    summary="API endpoint for dating application for people living with HIV/AIDs",
    version=version,
)

app.include_router(router, prefix=f"/api/{version}/books", tags=['Books'])
