import uuid
from contextlib import contextmanager

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Book, Borrowing, Member
from models.borrowing import RegisterBorrowingRequest


class BorrowingService:
    @staticmethod
    @contextmanager
    def transaction(session: Session):
        try:
            yield
            session.commit()
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def register_borrowing(db: Session, borrowing_request: RegisterBorrowingRequest):
        book = db.query(Book).filter(Book.id == borrowing_request.book_id).first()
        if not book or book.stock <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book is out of stock"
            )

        member = db.query(Member).filter(Member.id == borrowing_request.member_id).first()
        if not member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member not found"
            )

        borrow_count = db.query(func.count()).filter(
            Borrowing.member_id == borrowing_request.member_id,
            Borrowing.status == "BORROWED"
        ).scalar()
        if borrow_count >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Member cannot borrow anymore books"
            )

        with BorrowingService.transaction(db):
            book.stock -= 1
            borrowing_record = Borrowing(
                book_id=borrowing_request.book_id,
                member_id=borrowing_request.member_id,
                borrow_date=func.now()
            )
            db.add(borrowing_record)

        return {"message": "Book borrowed successfully!"}
    
    @staticmethod
    def return_book(id: uuid.UUID, db: Session):
        borrowing = db.query(Borrowing).filter(Borrowing.id == id, Borrowing.status == "BORROWED").first()
        if not borrowing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Borrowing id invalid"
            )

        book = db.query(Book).filter(Book.id == borrowing.book_id).first()

        with BorrowingService.transaction(db):
            book.stock += 1
            borrowing.status = "RETURNED"
            borrowing.return_date = func.now()

        return {"message": "Book returned successfully!"}