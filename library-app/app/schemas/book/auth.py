import re

from gettext import gettext as _
from unicode_tr import unicode_tr
from pydantic import EmailStr, field_validator

from app.helpers.validation_helper import check_user_password
from app.schemas.base_schema import BaseSchema


class EmailIn(BaseSchema):
    email: EmailStr

    @field_validator("email")
    def check_turkish_chars(cls, value):
        if re.search(r"[ÇçĞğİıÖöŞşÜü]", value):
            raise ValueError(_("Please enter a valid email address."))
        return value


class PasswordIn(BaseSchema):
    password: str

    @field_validator("password")
    def check_password(cls, passwd):
        return check_user_password(passwd)


class RegisterIn(EmailIn, PasswordIn):
    first_name: str
    last_name: str

    @field_validator("first_name")
    def check_first_name(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(
                _("Your name cannot contain numbers or special characters.")
            )
        return unicode_tr(v).lower().strip()

    @field_validator("last_name")
    def check_last_name(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError(
                _("Your surname cannot contain numbers or special characters.")
            )
        return unicode_tr(v).lower().strip()


class RegisterOut(EmailIn):
    first_name: str
    last_name: str
    is_admin: bool
