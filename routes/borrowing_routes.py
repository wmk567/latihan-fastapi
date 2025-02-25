import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.borrowing_controller import BorrowingController
from models.borrowing import RegisterBorrowingRequest

router = APIRouter(prefix="/borrowings", tags=["borrowings"])

@router.post("")
def register_borrowing(
    borrowing_request: RegisterBorrowingRequest,
    db: Session = Depends(get_db)
):
    return BorrowingController.register_borrowing(borrowing_request, db)
    
@router.put("/{id}/return")
def return_book(id: uuid.UUID, db: Session = Depends(get_db)):
    return BorrowingController.return_book(id, db)