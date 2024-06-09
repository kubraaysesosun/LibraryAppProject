from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.core import Base
from app.enums import Status

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.id == id, self.model.status == Status.active)
            .first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .filter(self.model.status == Status.active)
            .offset(skip)
            .limit(limit)
        )

    def create(
        self,
        db: Session,
        *,
        obj_in: Union[CreateSchemaType, dict],
        no_commit: bool = False,
        **kwargs,
    ) -> ModelType:
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        if no_commit:
            db.flush()
        else:
            db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def update(
        cls,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
        no_commit: bool = False,
        **kwargs,
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in update_data:
            if hasattr(db_obj, field):
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        if no_commit:
            db.flush()
        else:
            db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def delete(
        self, db: Session, *, id: int, no_commit: bool = False, **kwargs
    ) -> ModelType:
        obj = db.query(self.model).get(id)
        obj.status = Status.deleted
        if no_commit:
            db.flush()
        else:
            db.commit()
        db.refresh(obj)
        return obj

    def get_by_field(
        self, db: Session, field: str, val: str
    ) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(
                getattr(self.model, field) == val,
                self.model.status == Status.active,
            )
            .first()
        )

    def get_by_field_i(
        self, db: Session, field: str, val: str
    ) -> Optional[ModelType]:
        return (
            db.query(self.model)
            .filter(
                func.lower(getattr(self.model, field)) == val.lower(),
                self.model.status == Status.active,
            )
            .first()
        )

    def get_all_with_paginate(self, db: Session):
        q = db.query(self.model)
        if hasattr(self.model, "status"):
            q = q.filter(self.model.status != Status.deleted)

        return paginate(q)
