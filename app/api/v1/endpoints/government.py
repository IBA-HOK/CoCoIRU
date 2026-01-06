from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

# DB接続とCRUDロジックをインポート
from db.session import get_db
from db import crud_government

router = APIRouter()

# ---------------------------------------------------------
# レスポンス用のPydanticモデル (このファイル内だけで使用)
# ---------------------------------------------------------
class GovernmentRequestItem(BaseModel):
    request_id: int
    community_id: int
    request_content_id: int
    status: str| None = None
    created_at: str| None = None
    
    # 結合された情報
    community_name: str| None = None
    latitude: float | None = None
    longitude: float | None = None
    number: int| None = None
    item_name: str| None = None
    unit: str | None = None

    class Config:
        from_attributes = True

# ---------------------------------------------------------
# エンドポイント定義
# ---------------------------------------------------------
@router.get("/requests", response_model=List[GovernmentRequestItem])
def read_dashboard_requests(db: Session = Depends(get_db)):
    """
    行政ダッシュボード向け：全支援要請を詳細情報（名前など）付きで取得する。
    """
    requests = crud_government.get_dashboard_requests(db)
    return requests