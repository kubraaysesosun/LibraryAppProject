from app.enums.base_enum import BaseEnum


class Status(int, BaseEnum):
    active = 1
    passive = 0
    deleted = -1
