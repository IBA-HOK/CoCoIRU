from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.SpecialNotes)
def api_create_special_note(
    item: schemas.SpecialNotesCreate, db: Session = Depends(get_db)
):
    return crud.create_special_note(db=db, special_note=item)

@router.get("/", response_model=List[schemas.SpecialNotes])
def api_read_special_notes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_special_notes(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.SpecialNotes)
def api_read_special_note(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_special_note(db, special_notes_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SpecialNote not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.SpecialNotes)
def api_update_special_note(
    item_id: int, item: schemas.SpecialNotesCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_special_note(db, special_notes_id=item_id, special_note_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SpecialNote not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.SpecialNotes)
def api_delete_special_note(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_special_note(db, special_notes_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="SpecialNote not found")
    return db_item