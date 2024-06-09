from typing import Mapping

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.models import User
from app.schemas.book.book import (
    BookIn,
    BookOut,
    BorrowOut,
    BorrowedBookOut,
    RefundOut,
)
from app.views.v1.deps import (
    get_current_active_user,
    get_active_admin_user,
    valid_book_id,
)
from app.views.deps import get_db
from app.helpers.error_helper import Error, NotFound

router = APIRouter()


@router.post(
    "/",
    response_model=BookOut,
    summary="Add Book",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_active_admin_user)],
)
async def add_book(book: BookIn, db: Session = Depends(get_db)):
    is_exist_book = book_core.get_by_field(db=db, field="name", val=book.name)
    if is_exist_book:
        raise NotFound(Error.book_already_exist)
    return book_core.create(db=db, obj_in=book)


@router.get(
    "/borrowed_books",
    response_model=Page[BorrowedBookOut],
    summary="Borrowed Books",
    dependencies=[Depends(get_current_active_user)],
)
async def get_borrowed_books(
    db: Session = Depends(get_db),
):
    return paginate(book_core.get_borrowed_books(db))


@router.get(
    "/overdue_books",
    response_model=Page[BorrowedBookOut],
    summary="Overdue Books",
    dependencies=[Depends(get_current_active_user)],
)
async def get_overdue_books(
    db: Session = Depends(get_db),
):
    return paginate(book_core.get_overdue_books(db))


@router.get(
    "/{book_id}",
    response_model=BookOut,
    summary="Retrieve Book",
    dependencies=[Depends(get_current_active_user)],
)
async def retrieve_book(book: Mapping = Depends(valid_book_id)):
    return book


@router.get(
    "/",
    response_model=Page[BookOut],
    summary="Get Books",
    dependencies=[Depends(get_current_active_user)],
)
async def get_books(db: Session = Depends(get_db)):
    return paginate(book_core.get_multi(db=db))


@router.put(
    "/{book_id}",
    response_model=BookOut,
    summary="Update Book",
    dependencies=[Depends(get_active_admin_user)],
)
async def put_book(
    book_in: BookIn,
    book: Mapping = Depends(valid_book_id),
    db: Session = Depends(get_db),
):
    return book_core.update(db=db, db_obj=book, obj_in=book_in)


@router.delete(
    "/{book_id}",
    summary="Delete Book",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_active_admin_user)],
)
async def delete_book(
    book: Mapping = Depends(valid_book_id), db: Session = Depends(get_db)
):
    book_core.delete(db=db, book=book)
    return


@router.post(
    "/{book_id}/borrow",
    response_model=BorrowOut,
    summary="Borrow Book",
    status_code=status.HTTP_201_CREATED,
)
async def borrow_book(
    book: Mapping = Depends(valid_book_id),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return book_core.borrow_book(db, book, current_user)


@router.post(
    "/{book_id}/refund",
    response_model=RefundOut,
    summary="Refund Book",
    status_code=status.HTTP_200_OK,
)
async def refund_book(
    book: Mapping = Depends(valid_book_id),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return book_core.refund_book(db, book, current_user)
