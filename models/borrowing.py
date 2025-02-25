# app/models/borrowing.py
import uuid
from enum import Enum as PyEnum

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base


class BorrowingStatus(PyEnum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"

class Borrowing(Base):
    __tablename__ = "borrowings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = Column(UUID(as_uuid=True), ForeignKey("books.id"), nullable=False)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    status = Column(Enum(BorrowingStatus), default=BorrowingStatus.BORROWED)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    book = relationship("Book", back_populates="borrowings")
    member = relationship("Member", back_populates="borrowings")

class RegisterBorrowingRequest(BaseModel):
    book_id: uuid.UUID
    member_id: uuid.UUID