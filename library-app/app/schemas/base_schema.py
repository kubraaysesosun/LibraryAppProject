from typing import Generic, Optional, TypeVar

from fastapi_pagination import Page as _Page
from pydantic import BaseModel, Field

from app.enums import BaseEnum


class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            BaseEnum: lambda g: g.name,
        }


T = TypeVar("T")


class PageBase(BaseSchema, _Page[T]):
    pass


Page = PageBase.with_custom_options(
    size=Field(10, ge=1, le=100),
)


class ErrorData(BaseSchema):
    code: int
    message: str
    fields: Optional[dict]


class ResponseSchema(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    error: Optional[ErrorData] = None
    data: T

    class Config:
        populate_by_name = True
        json_encoders = {
            BaseEnum: lambda g: g.name,
        }


class InternalServerErrorData(BaseSchema):
    code: int = 500
    message: str = "Internal server error"
    fields: Optional[dict] = None


class InternalServerResponseSchema(BaseModel, Generic[T]):
    success: bool = False
    message: str = "Internal server error"
    error: Optional[InternalServerErrorData]
    data: Optional[dict] = None
