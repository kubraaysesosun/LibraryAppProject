from typing import Mapping

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.book import book_core
from app.core.user import user_core
from app.enums import Status
from app.helpers.error_helper import Error, Forbidden, Unauthorized, NotFound
from app.helpers.secret_helper import SecretHelper
from app.models.user import User
from app.views.deps import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    payload = SecretHelper.verify_token(token=token)
    user_id: int = payload.get("user_id")

    user = user_core.get_by_id(db=db, user_id=user_id)
    if user is None:
        raise Unauthorized(Error.could_not_validate_credentials)

    return user


def get_current_active_user(
    request: Request, current_user: User = Depends(get_current_user)
) -> User:
    if current_user.status != Status.active:
        raise Forbidden(Error.user_deactivated)
    return current_user


def get_active_admin_user(
    request: Request, current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_admin:
        raise Forbidden(Error.admin_user_required)
    return current_user


def valid_book_id(book_id: int, db: Session = Depends(get_db)) -> Mapping:
    book = book_core.get(db=db, id=book_id)
    if not book:
        raise NotFound(Error.book_not_found)

    return book
