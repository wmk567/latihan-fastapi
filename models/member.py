import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base

from .book import BookData


class Member(Base):
    __tablename__ = "members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    address = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    borrowings = relationship("Borrowing", back_populates="member")

class RegisterMemberRequest(BaseModel):
    name: str
    email: str
    phone: str
    address: str

class MemberBorrowingResponse(BaseModel):
    id: uuid.UUID
    borrow_date: datetime
    return_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime
    book: BookData

class PaginationResponse(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int

class MemberBorrowingPaginatedResponse(BaseModel):
    data: List[MemberBorrowingResponse]
    pagination: PaginationResponse