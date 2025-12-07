from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Members)
def api_create_member(
    item: schemas.MembersCreate, db: Session = Depends(get_db)
):
    return crud.create_member(db=db, member=item)

@router.get("/", response_model=List[schemas.Members])
def api_read_members(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_members(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.Members)
def api_read_member(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_member(db, member_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Members)
def api_update_member(
    item_id: int, item: schemas.MembersCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_member(db, member_id=item_id, member_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.Members)
def api_delete_member(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_member(db, member_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return db_item