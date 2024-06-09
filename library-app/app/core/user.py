from typing import Optional

from sqlalchemy.orm import Session
from datetime import datetime

from app.config import settings
from app.core.crud_base import CRUDBase
from app.helpers.hash_helper import HashHelper
from app.helpers.secret_helper import secret_helper
from app.models import User

from app.schemas.book.auth import RegisterIn


class UserCore(CRUDBase[User, None, None]):

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email).first()
        return user

    @staticmethod
    def user_register(
        db: Session, register_schema: RegisterIn, is_admin: bool = False
    ):
        user = User(
            first_name=register_schema.first_name,
            last_name=register_schema.last_name,
            email=register_schema.email,
            password=HashHelper.get_password_hash(register_schema.password),
            is_admin=is_admin,
        )
        db.add(user)
        db.flush()
        db.commit()
        return user

    @staticmethod
    def get_token(user: User) -> tuple[datetime, str]:
        exp_date = secret_helper.get_expire_date(settings.JWT_EXPIRES_TIME)
        token = secret_helper.create_access_token(
            {"email": user.email, "is_admin": user.is_admin}
        )

        return exp_date, token

    @staticmethod
    def user_login(db: Session, user: User):
        access_token = secret_helper.create_access_token({"user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}


user_core = UserCore(User)
