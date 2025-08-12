# apps/api/app/routers/router_factory.py
from typing import Callable, Optional, Type, List, TypeVar
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.abstract import (
    NotFoundException,
    IntegrityConflictException,
    CrudException,
)

CreateSchema = TypeVar("CreateSchema", bound=BaseModel)
UpdateSchema = TypeVar("UpdateSchema", bound=BaseModel)
ReadSchema = TypeVar("ReadSchema", bound=BaseModel)


def RouterFactory(
    *,
    name: str,
    pk_type: type,
    create_schema: Type[CreateSchema],
    update_schema: Type[UpdateSchema],
    read_schema: Type[ReadSchema],
    repo,  # AbstractRepository(model) instance
    pk_field: str = "id",
    extra_routes: Optional[Callable[[APIRouter], None]] = None,
) -> APIRouter:
    """
    Minimal, safe CRUD router for POC: list (pagination), get, create, update, delete.
    """
    tag = name.capitalize()
    router = APIRouter(prefix=f"/{name}", tags=[tag])

    if extra_routes:
        extra_routes(router)

    @router.get("/", response_model=List[read_schema], response_model_exclude_none=True)
    def list_items(
        db: Session = Depends(get_db),
        limit: int = Query(100, ge=1, le=1000),
        offset: int = Query(0, ge=0),
    ):
        try:
            return repo.list_all(session=db, limit=limit, offset=offset)
        except CrudException as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get(
        "/{item_id}", response_model=read_schema, response_model_exclude_none=True
    )
    def get_item(item_id: pk_type, db: Session = Depends(get_db)):
        try:
            return repo.get_one_by_id(db, item_id, column=pk_field)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except CrudException as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.post(
        "/",
        response_model=read_schema,
        response_model_exclude_none=True,
        status_code=status.HTTP_201_CREATED,
    )
    def create_item(payload: create_schema, db: Session = Depends(get_db)):
        try:
            return repo.create(db, payload)
        except IntegrityConflictException as e:
            raise HTTPException(status_code=409, detail=str(e))
        except CrudException as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.put(
        "/{item_id}", response_model=read_schema, response_model_exclude_none=True
    )
    def update_item(
        item_id: pk_type, payload: update_schema, db: Session = Depends(get_db)
    ):
        try:
            return repo.update_by_id(db, item_id, payload, column=pk_field)
        except NotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except IntegrityConflictException as e:
            raise HTTPException(status_code=409, detail=str(e))
        except CrudException as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: pk_type, db: Session = Depends(get_db)):
        try:
            rows = repo.remove_by_id(db, item_id, column=pk_field)
            if rows == 0:
                raise HTTPException(status_code=404, detail=f"{name} not found")
        except CrudException as e:
            raise HTTPException(status_code=400, detail=str(e))

    return router
