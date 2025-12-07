from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas
from app.core.security import require_token

router = APIRouter(dependencies=[Depends(require_token)])

@router.post("/", response_model=schemas.Items)
def api_create_item(
    item: schemas.ItemsCreate, db: Session = Depends(get_db)
):
    return crud.create_item(db=db, item=item)

@router.get("/", response_model=List[schemas.Items])
def api_read_items(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.Items)
def api_read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Items)
def api_update_item(
    item_id: int, item: schemas.ItemsCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_item(db, item_id=item_id, item_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.Items)
def api_delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item