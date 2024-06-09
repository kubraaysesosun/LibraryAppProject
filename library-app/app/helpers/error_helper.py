from enum import IntEnum
from gettext import gettext as _
from typing import Optional, Union

from fastapi import HTTPException, status


class Error(IntEnum):
    def __new__(cls, value, phrase):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj.phrase = phrase
        return obj

    # book
    book_already_exist = 100, _("The book is already registered.")
    book_not_found = 101, _("No book found.")
    book_not_available = 102, ("Book is not available.")
    book_not_borrowed = 103, ("Book is not borrowed.")
    user_not_borrowed_that_book = 104, ("You did not borrow this book.")
    borrowed_book_cannot_delete = 105, ("Borrowed book cannot be deleted.")

    # auth
    email_already_exists = 200, _(
        "E-posta adresi hatalı. Bilgilerinizi kontrol edip lütfen yeniden deneyin."
    )
    user_deactivated = 201, _("No user found.")
    invalid_login = 202, _("User email or password is incorrect.")
    invalid_access_session = 203, _(
        "Your session has ended due to a long period of inactivity. Please log in again."
    )
    could_not_validate_credentials = 204, _("Could not validate credentials")
    admin_user_required = 205, _("Admin user required")


class BadRequest(HTTPException):
    def __init__(
        self, error: Union[Error, str], headers: Optional[dict] = None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
            headers=headers,
        )


class Unauthorized(HTTPException):
    def __init__(
        self,
        error: Union[Error, str],
        headers: Optional[dict] = None,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error,
            headers=headers or {"WWW-Authenticate": "Bearer"},
        )


class NotFound(HTTPException):
    def __init__(
        self, error: Union[Error, str], headers: Optional[dict] = None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
            headers=headers,
        )


class Forbidden(HTTPException):
    def __init__(
        self, error: Union[Error, str], headers: Optional[dict] = None
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error,
            headers=headers,
        )


class UnprocessableEntity(HTTPException):
    def __init__(
        self, error: Union[Error, str], headers: Optional[dict] = None
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error,
            headers=headers,
        )
