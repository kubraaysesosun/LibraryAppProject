import re


def check_user_password(password: str):
    if not re.match(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$!@%^&*#]).{8,}$", password
    ):
        raise ValueError(
            "Your password must contain at least one lowercase letter, one uppercase letter, one number and one special character. Your password must also be at least 8 characters long."
        )
    return password
