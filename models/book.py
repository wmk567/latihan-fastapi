import uuid
from typing import List

from pydantic import BaseModel
from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from config.database import Base


class Book(Base):
    __tablename__ = 'books'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    published_year = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    isbn = Column(String(13), unique=True, nullable=False)

    borrowings = relationship("Borrowing", back_populates="book")

class BookData(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    published_year: int
    stock: int
    isbn: str
    available: bool

class PaginationResponse(BaseModel):
    total: int
    page: int
    limit: int
    totalPages: int

class BookResponse(BaseModel):
    data: List[BookData]
    pagination: PaginationResponse