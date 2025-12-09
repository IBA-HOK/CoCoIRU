from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from db.session import get_db
from db import crud, schemas

router = APIRouter()


@router.get("/items", response_model=List[schemas.Items], tags=["Public"])
def api_public_get_supported_items(db: Session = Depends(get_db)):
    """RequestContent に登録されている支援可能品目の一覧を返す（認証不要）"""
    return crud.get_supported_items(db)
