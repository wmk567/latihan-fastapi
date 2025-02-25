from typing import Optional

from sqlalchemy.orm import Session

from models.book import BookResponse, PaginationResponse
from services.book_service import BookService


class BookController:
    @staticmethod
    def get_books(db: Session, title: Optional[str] = None, author: Optional[str] = None, page: int = 1, limit: int = 10):
        result = BookService.get_books(db, title, author, page, limit)
        
        return BookResponse(
            data=result["data"],
            pagination=PaginationResponse(
                total=result["pagination"]["total"],
                page=result["pagination"]["page"],
                limit=result["pagination"]["limit"],
                totalPages=result["pagination"]["totalPages"]
            )
        )