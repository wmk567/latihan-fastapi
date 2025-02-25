from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.book_controller import BookController
from models.book import BookResponse

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=BookResponse)
def get_books(
    title: Optional[str] = None, 
    author: Optional[str] = None,
    page: int = 1, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return BookController.get_books(db, title, author, page, limit)
