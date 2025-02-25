from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.book import Book, BookData


class BookService:
    @staticmethod
    def get_books(db: Session, title: Optional[str] = None, author: Optional[str] = None, page: int = 1, limit: int = 10):
        query = select(Book)

        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))

        result = db.execute(query)
        books = result.scalars().all()

        total = len(books)
        total_pages = (total // limit) + (1 if total % limit > 0 else 0)
        start = (page - 1) * limit
        end = start + limit
        paginated_books = books[start:end]

        book_data_list = [BookData(
            id=book.id,
            title=book.title,
            author=book.author,
            published_year=book.published_year,
            stock=book.stock,
            isbn=book.isbn,
            available=book.stock > 0
        ) for book in paginated_books]

        return {
            "data": book_data_list,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": total_pages
            }
        }