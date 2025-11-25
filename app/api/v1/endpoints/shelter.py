from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Shelter)
def api_create_shelter(
    item: schemas.ShelterCreate, db: Session = Depends(get_db)
):
    return crud.create_shelter(db=db, shelter=item)

@router.get("/", response_model=List[schemas.Shelter])
def api_read_shelters(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_shelters(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.Shelter)
def api_read_shelter(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_shelter(db, shelter_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Shelter)
def api_update_shelter(
    item_id: int, item: schemas.ShelterCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_shelter(db, shelter_id=item_id, shelter_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.Shelter)
def api_delete_shelter(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_shelter(db, shelter_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Shelter not found")
    return db_item