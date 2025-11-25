from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas
from app.core.security import require_token, require_gov_role

router = APIRouter()

@router.post("/", response_model=schemas.SupportRequest, dependencies=[Depends(require_token)])
def api_create_support_request(
    item: schemas.SupportRequestCreate, db: Session = Depends(get_db)
):
    return crud.create_support_request(db=db, support_request=item)

@router.get("/", response_model=List[schemas.SupportRequest], dependencies=[Depends(require_gov_role)])
def api_read_support_requests(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """全支援要請一覧を取得（gov専用）"""
    return crud.get_support_requests(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.SupportRequest, dependencies=[Depends(require_token)])
def api_read_support_request(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_support_request(db, request_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SupportRequest not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.SupportRequest, dependencies=[Depends(require_token)])
def api_update_support_request(
    item_id: int, item: schemas.SupportRequestCreate, db: Session = Depends(get_db)
):
    
    db_item = crud.update_support_request(db, request_id=item_id, support_request_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SupportRequest not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.SupportRequest, dependencies=[Depends(require_token)])
def api_delete_support_request(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_support_request(db, request_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SupportRequest not found")
    return db_item