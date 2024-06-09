from datetime import timedelta, date

from sqlalchemy import (
    Column,
    Enum,
    String,
    Integer,
    ForeignKey,
    Date,
    Boolean,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from app.config import settings
from app.database.core import Base
from app.enums import Status


class Book(Base):
    __tablename__ = "book"

    name = Column(String(100), nullable=False, unique=True)
    author = Column(String(32), nullable=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)
    is_borrowed = Column(Boolean, default=False, index=True)

    borrows = relationship("Borrow", back_populates="book")


class Borrow(Base):
    __tablename__ = "borrow"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    is_refunded = Column(Boolean, default=False)
    borrowed_date = Column(Date, index=True, default=date.today)
    refunded_date = Column(Date, default=None)
    expire_date = Column(Date)

    book = relationship("Book", back_populates="borrows")
    user = relationship("User", back_populates="borrows")

    __table_args__ = (
        Index(
            "idx_borrow_is_refunded_book_user",
            "is_refunded",
            "book_id",
            "user_id",
        ),
    )

    def __init__(
        self, book_id: int, user_id: int, borrow_date: date = date.today()
    ):
        self.book_id = book_id
        self.user_id = user_id
        self.borrowed_date = borrow_date
        self.expire_date = borrow_date + timedelta(
            days=settings.BORROW_TIME_IN_DAY
        )
