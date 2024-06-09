from datetime import date
from typing import List

from sqlalchemy.orm import Session

from app.core.crud_base import CRUDBase
from app.helpers.error_helper import BadRequest, Error

from app.models import Book, User
from app.models.book import Borrow
from app.schemas.book.book import BookIn


class BookCore(CRUDBase[Book, BookIn, BookIn]):
    def is_book_available_to_borrow(self, book: Book) -> bool:
        return not book.is_borrowed

    def borrow_book(self, db: Session, book: Book, user: User) -> Borrow:
        if not self.is_book_available_to_borrow(book):
            raise BadRequest(Error.book_not_available)

        borrow = Borrow(book_id=book.id, user_id=user.id)

        book.is_borrowed = True

        db.add_all((borrow, book))
        db.commit()
        return borrow

    def refund_book(self, db: Session, book: Book, user: User) -> Borrow:
        if self.is_book_available_to_borrow(book):
            raise BadRequest(Error.book_not_borrowed)

        borrow = (
            db.query(Borrow)
            .filter(
                Borrow.is_refunded == False,
                Borrow.book_id == book.id,
                Borrow.user_id == user.id,
            )
            .first()
        )

        if not borrow:
            raise BadRequest(Error.user_not_borrowed_that_book)

        borrow.is_refunded = True
        borrow.refunded_date = date.today()
        book.is_borrowed = False

        db.add_all((borrow, book))
        db.commit()

        return borrow

    def delete(self, db: Session, book: Book, *args, **kwargs):
        if book.is_borrowed:
            raise BadRequest(Error.borrowed_book_cannot_delete)
        return super(BookCore, self).delete(db=db, id=book.id)

    @staticmethod
    def get_borrowed_books(db: Session) -> List[Book]:
        return db.query(Book).filter(Book.is_borrowed == True)

    @staticmethod
    def get_overdue_books(db: Session) -> List[Book]:
        current_date = date.today()
        overdue_books = (
            db.query(Book)
            .join(Borrow, Book.id == Borrow.book_id)
            .filter(Book.is_borrowed == True, Borrow.is_refunded == False)
            .group_by(Book.id, Borrow.expire_date)
            .having(Borrow.expire_date < current_date)
        )
        return overdue_books


book_core = BookCore(Book)
