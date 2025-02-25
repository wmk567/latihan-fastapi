import re
import uuid
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.book import Book, BookData
from models.borrowing import Borrowing
from models.member import (Member, MemberBorrowingResponse,
                           RegisterMemberRequest)


class MemberService:

    @staticmethod
    def register_member(
        member_request: RegisterMemberRequest,
        db: Session
    ):
        if (not member_request.name.strip() or 
            not member_request.email.strip() or 
            not member_request.phone.strip() or
            not member_request.address.strip() ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All fields are required"
            )

        existing_member = db.query(Member).filter(Member.email == member_request.email).first()
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", member_request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is invalid"
            )

        if not re.match(r"^0\d{11}$", member_request.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number invalid"
            )


        new_member = Member(
            name=member_request.name,
            email=member_request.email,
            phone=member_request.phone,
            address=member_request.address
        )

        try:
            db.add(new_member)
            db.commit()
            db.refresh(new_member)
        except Exception as e:
            db.rollback()
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to add member"
            )

        return {"message": "Member successfully registered", "member_id": new_member.id}
    
    def get_borrowing_history(
        db: Session,
        id:uuid.UUID,
        status: Optional[str] = None,
        page: int = 1, 
        limit: int = 10
    ):
        query = select(Borrowing).filter(Borrowing.member_id == id)

        if status:
            query = query.filter(Borrowing.status == status)

        query = query.join(Book)
        result = db.execute(query)
        member_borrowings = result.scalars().all()

        total = len(member_borrowings)
        total_pages = (total // limit) + (1 if total % limit > 0 else 0)
        start = (page - 1) * limit
        end = start + limit
        paginated_member_borrowings = member_borrowings[start:end]

        member_borrowings_list = [MemberBorrowingResponse(
            id=borrow.id,
            borrow_date=borrow.borrow_date,
            return_date=borrow.return_date,
            status=borrow.status,
            created_at=borrow.created_at,
            updated_at=borrow.updated_at,
            book=BookData(
                id=borrow.book.id,
                title=borrow.book.title,
                author=borrow.book.author,
                published_year=borrow.book.published_year,
                stock=borrow.book.stock,
                isbn=borrow.book.isbn,
                available=borrow.book.stock > 0
            )
        ) for borrow in paginated_member_borrowings]

        return {
            "data": member_borrowings_list,
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": total_pages
            }
        }