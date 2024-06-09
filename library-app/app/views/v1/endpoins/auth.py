from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.core.user import user_core
from app.enums import Status
from app.helpers.error_helper import BadRequest, Error
from app.helpers.hash_helper import HashHelper
from app.schemas.book.auth import RegisterIn, RegisterOut
from app.views.deps import get_db

router = APIRouter()


@router.post(
    "/register",
    response_model=RegisterOut,
    summary="User Register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    register_schema: RegisterIn,
    db: Session = Depends(get_db),
):
    check_user_email = user_core.get_by_email(db, email=register_schema.email)
    if check_user_email:
        raise BadRequest(Error.email_already_exists)

    return user_core.user_register(register_schema=register_schema, db=db)


@router.post("/login", summary="User Login")
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = user_core.get_by_email(db, email=form_data.username)
    if not user or user.status != Status.active:
        raise BadRequest(Error.invalid_login)

    if not user or not HashHelper.verify(user.password, form_data.password):
        raise BadRequest(Error.invalid_login)

    return user_core.user_login(db=db, user=user)
