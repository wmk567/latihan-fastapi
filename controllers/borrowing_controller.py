import uuid

from sqlalchemy.orm import Session

from services.borrowing_service import (BorrowingService,
                                        RegisterBorrowingRequest)


class BorrowingController:
    @staticmethod
    def register_borrowing(borrowing_request: RegisterBorrowingRequest, db: Session):
        return BorrowingService.register_borrowing(db, borrowing_request)
    
    @staticmethod
    def return_book(id: uuid.UUID, db: Session):
        return BorrowingService.return_book(id, db)