import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.member_controller import MemberController
from models.member import RegisterMemberRequest

router = APIRouter(prefix="/members", tags=["members"])

@router.post("")
def register_member(
    member_request: RegisterMemberRequest,
    db: Session = Depends(get_db)
):
    return MemberController.register_member(member_request, db)

@router.get("/{id}/borrowings")
def get_borrowing_history(
    id:uuid.UUID,
    status: Optional[str] = None,
    page: int = 1, 
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return MemberController.get_borrowing_history(db, id, status, page, limit)