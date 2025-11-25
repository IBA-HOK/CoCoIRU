from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.RequestContent)
def api_create_request_content(
    item: schemas.RequestContentCreate, db: Session = Depends(get_db)
):
    return crud.create_request_content(db=db, request_content=item)

@router.get("/", response_model=List[schemas.RequestContent])
def api_read_request_contents(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_request_contents(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.RequestContent)
def api_read_request_content(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_request_content(db, request_content_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="RequestContent not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.RequestContent)
def api_update_request_content(
    item_id: int, item: schemas.RequestContentCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_request_content(db, request_content_id=item_id, request_content_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="RequestContent not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.RequestContent)
def api_delete_request_content(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_request_content(db, request_content_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="RequestContent not found")
    return db_item