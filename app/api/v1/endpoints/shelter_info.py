from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas
from app.core.security import require_token

router = APIRouter(dependencies=[Depends(require_token)])

@router.post("/", response_model=schemas.ShelterInfo)
def api_create_shelter_info(
    item: schemas.ShelterInfoCreate, db: Session = Depends(get_db)
):
    return crud.create_shelter_info(db=db, shelter_info=item)

@router.get("/", response_model=List[schemas.ShelterInfo])
def api_read_shelter_infos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_shelter_infos(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.ShelterInfo)
def api_read_shelter_info(item_id: int, db: Session = Depends(get_db)):
    # PK名は shelter_info_id
    db_item = crud.get_shelter_info(db, shelter_info_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="ShelterInfo not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.ShelterInfo)
def api_update_shelter_info(
    item_id: int, item: schemas.ShelterInfoCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_shelter_info(db, shelter_info_id=item_id, shelter_info_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="ShelterInfo not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.ShelterInfo)
def api_delete_shelter_info(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_shelter_info(db, shelter_info_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="ShelterInfo not found")
    return db_item