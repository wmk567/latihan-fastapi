import uuid
from typing import Optional

from sqlalchemy.orm import Session

from models.member import (MemberBorrowingPaginatedResponse,
                           PaginationResponse, RegisterMemberRequest)
from services.member_service import MemberService


class MemberController:
    @staticmethod
    def register_member(
        member_request: RegisterMemberRequest,
        db: Session
    ):
        return MemberService.register_member(member_request, db)
    
    @staticmethod
    def get_borrowing_history(
        db: Session,
        id:uuid.UUID,
        status: Optional[str] = None,
        page: int = 1, 
        limit: int = 10,
    ):
        result = MemberService.get_borrowing_history(db, id, status, page, limit)
        return MemberBorrowingPaginatedResponse(
            data=result["data"],
            pagination=PaginationResponse(
                total=result["pagination"]["total"],
                page=result["pagination"]["page"],
                limit=result["pagination"]["limit"],
                totalPages=result["pagination"]["totalPages"]
            )
        )
        