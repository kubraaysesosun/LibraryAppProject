from sqlalchemy import Column, Enum, String, Boolean
from sqlalchemy.orm import column_property, relationship

from app.database.core import Base
from app.enums import Status


class User(Base):
    __tablename__ = "user"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    full_name = column_property(first_name + " " + last_name)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    status = Column(Enum(Status), nullable=False, default=Status.active)

    borrows = relationship("Borrow", back_populates="user")
