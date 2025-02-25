from fastapi import APIRouter, FastAPI

from config.database import Base, engine
from models import Book, Borrowing, Member
from routes.book_routes import router as book_router
from routes.borrowing_routes import router as borrowing_router
from routes.member_routes import router as member_router

app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(book_router)
api_router.include_router(member_router)
api_router.include_router(borrowing_router)

app.include_router(api_router)
Base.metadata.create_all(bind=engine)

