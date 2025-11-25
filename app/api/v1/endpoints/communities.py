from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.session import get_db
from db import crud, schemas
from app.core.security import require_token, require_gov_role

router = APIRouter()

@router.post("/", response_model=schemas.Communities)
def api_create_community(
    item: schemas.CommunitiesCreate, db: Session = Depends(get_db)
):
    """
    コミュニティを作成します。
    注意: 最初のコミュニティ作成を可能にするため、このエンドポイントのみ認証不要です。
    """
    return crud.create_community(db=db, community=item)

@router.get("/", response_model=List[schemas.Communities], dependencies=[Depends(require_gov_role)])
def api_read_communities(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """全コミュニティ一覧を取得（gov専用）"""
    return crud.get_communities(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.Communities, dependencies=[Depends(require_token)])
def api_read_community(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_community(db, community_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Community not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Communities, dependencies=[Depends(require_token)])
def api_update_community(
    item_id: int, item: schemas.CommunitiesCreate, db: Session = Depends(get_db)
):
    db_item = crud.update_community(db, community_id=item_id, community_update=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Community not found")
    return db_item

@router.delete("/{item_id}", response_model=schemas.Communities, dependencies=[Depends(require_token)])
def api_delete_community(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_community(db, community_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Community not found")
    return db_item