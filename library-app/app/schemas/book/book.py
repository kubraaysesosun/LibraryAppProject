from datetime import date
from app.schemas.base_schema import BaseSchema


class BookIn(BaseSchema):
    name: str
    author: str


class BaseBookOut(BaseSchema):
    id: int
    name: str
    author: str
    status: int


class BookOut(BaseBookOut):
    is_borrowed: bool


class BorrowedBookOut(BaseBookOut):
    pass


class BorrowOut(BaseSchema):
    id: int
    book: BorrowedBookOut
    borrowed_date: date
    expire_date: date


class RefundOut(BaseSchema):
    id: int
    book: BorrowedBookOut
    borrowed_date: date
    expire_date: date
    refunded_date: date
