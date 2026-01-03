from fastapi import FastAPI
from src.books.routes import router
from contextlib import asynccontextmanager
from src.db.main import init_db

# lets determine qhich code will run at the start of the application and whhich wont run at the start of the application by using the lifespan

@asynccontextmanager
async def life_span(app: FastAPI):
    # Code to run at startup
    print("Server is starting up...")
    await init_db()
    yield
    # Code to run at shutdown
    print("Server is shutting down...")


version = "v1"

app = FastAPI(
    lifespan=life_span,
    title='PL Connect API endpoints',
    description="This endpoints will be used for the development of PL connect mobile application for people living with HIV/AIDS",
    summary="API endpoint for dating application for people living with HIV/AIDs",
    version=version,
)

app.include_router(router, prefix=f"/api/{version}/books", tags=['Books'])
