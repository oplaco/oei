# apps/api/app/repositories/base.py
from __future__ import annotations
from typing import Any, Optional, Sequence, Type, TypeVar, Generic
from pydantic import BaseModel
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate", bound=BaseModel)
TUpdate = TypeVar("TUpdate", bound=BaseModel)


class CrudException(Exception): ...


class IntegrityConflictException(CrudException): ...


class NotFoundException(CrudException): ...


def AbstractRepository(model: Type[TModel]):
    class Repo(Generic[TModel, TCreate, TUpdate]):

        # CREATE
        @classmethod
        def create(
            cls, session: Session, data: TCreate, *, commit: bool = True
        ) -> TModel:
            try:
                obj = cls.model(**data.model_dump())
                session.add(obj)
                if commit:
                    session.commit()
                    session.refresh(obj)
                return obj
            except IntegrityError as e:
                session.rollback()
                raise IntegrityConflictException(str(e)) from e
            except Exception as e:
                session.rollback()
                raise CrudException(f"Create failed: {e}") from e

        # READ ALL (optional pagination only)
        @classmethod
        def list_all(
            cls,
            session: Session,
            *,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
        ) -> list[TModel]:
            try:
                stmt = select(cls.model)
                if offset is not None:
                    stmt = stmt.offset(offset)
                if limit is not None:
                    stmt = stmt.limit(limit)
                return session.execute(stmt).scalars().all()
            except Exception as e:
                raise CrudException(f"List failed: {e}") from e

        # READ ONE
        @classmethod
        def get_one_by_id(
            cls, session: Session, id_: Any, column: str = "id"
        ) -> TModel:
            if column == "id":
                obj = session.get(cls.model, id_)
            else:
                try:
                    col = getattr(cls.model, column)
                except AttributeError:
                    raise CrudException(
                        f"Column {column} not found on {cls.model.__tablename__}."
                    )
                obj = session.execute(
                    select(cls.model).where(col == id_)
                ).scalar_one_or_none()
            if not obj:
                raise NotFoundException(
                    f"{cls.model.__tablename__} with {column}={id_} not found."
                )
            return obj

        # UPDATE
        @classmethod
        def update_by_id(
            cls,
            session: Session,
            id_: Any,
            data: TUpdate,
            *,
            commit: bool = True,
            column: str = "id",
        ) -> TModel:
            obj = cls.get_one_by_id(session, id_, column)
            for k, v in data.model_dump(exclude_unset=True).items():
                setattr(obj, k, v)
            try:
                if commit:
                    session.commit()
                    session.refresh(obj)
                return obj
            except IntegrityError as e:
                session.rollback()
                raise IntegrityConflictException(str(e)) from e
            except Exception as e:
                session.rollback()
                raise CrudException(f"Update failed: {e}") from e

        # DELETE
        @classmethod
        def remove_by_id(
            cls, session: Session, id_: Any, *, commit: bool = True, column: str = "id"
        ) -> int:
            try:
                col = getattr(cls.model, column)
            except AttributeError:
                raise CrudException(
                    f"Column {column} not found on {cls.model.__tablename__}."
                )
            result = session.execute(delete(cls.model).where(col == id_))
            if commit:
                session.commit()
            return result.rowcount or 0

    Repo.model = model
    return Repo
