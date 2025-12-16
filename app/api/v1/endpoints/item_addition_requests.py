from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from db import crud, schemas
from app.core.security import require_token, require_gov_role

router = APIRouter()


def _ensure_create_update_allowed(token_data: dict):
    role = token_data.get("role")
    if role in ("admin", "gov", "community"):
        return
    raise HTTPException(status_code=403, detail="Insufficient permissions")


@router.post("/", response_model=schemas.ItemAdditionRequests)
def api_create_item_addition_request(
    item_req: schemas.ItemAdditionRequestsCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_token),
):
    _ensure_create_update_allowed(token_data)
    return crud.create_item_addition_request(db=db, item_req=item_req)


@router.get("/", response_model=List[schemas.ItemAdditionRequests], dependencies=[Depends(require_gov_role)])
def api_read_item_addition_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_item_addition_requests(db=db, skip=skip, limit=limit)


@router.get("/{add_req_id}", response_model=schemas.ItemAdditionRequests, dependencies=[Depends(require_gov_role)])
def api_read_item_addition_request(add_req_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_addition_request(db, add_req_id=add_req_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item addition request not found")
    return db_item


@router.put("/{add_req_id}", response_model=schemas.ItemAdditionRequests)
def api_update_item_addition_request(
    add_req_id: int,
    item_req: schemas.ItemAdditionRequestsCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(require_token),
):
    _ensure_create_update_allowed(token_data)
    db_item = crud.update_item_addition_request(db, add_req_id=add_req_id, item_req_update=item_req)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item addition request not found")
    return db_item


@router.delete("/{add_req_id}", response_model=schemas.ItemAdditionRequests, dependencies=[Depends(require_gov_role)])
def api_delete_item_addition_request(add_req_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item_addition_request(db, add_req_id=add_req_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item addition request not found")
    return db_item
