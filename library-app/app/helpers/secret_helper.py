from datetime import datetime, timedelta
from typing import Optional

import jwt

from app.config import settings
from app.helpers.error_helper import Unauthorized, Error


class SecretHelper:
    def __init__(self):
        self.security_context = None

    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_jwt_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                seconds=settings.JWT_EXPIRES_TIME
            )

        to_jwt_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_jwt_encode,
            settings.SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        try:
            data = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                verify=True,
            )
            if data is None:
                raise Unauthorized(Error.could_not_validate_credentials)
            return data
        except Exception:
            raise Unauthorized(Error.could_not_validate_credentials)

    @staticmethod
    def get_expire_date(second: int):
        return datetime.now() + timedelta(seconds=second)


secret_helper = SecretHelper()
