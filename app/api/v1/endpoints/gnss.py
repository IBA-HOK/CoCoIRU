from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import math

from db.session import get_db
from db.models import Communities
from db import schemas           # (重要) ご自身のCommunityスキーマをインポートしてください
from app.core.security import require_token

router = APIRouter(dependencies=[Depends(require_token)])

# 地球の半径 (km)
EARTH_RADIUS_KM = 6371.0

@router.get("/nearby", response_model=List[schemas.Communities]) # スキーマを指定
async def get_locations(
    latitude: float, 
    longitude: float, 
    range: float,
    db: Session = Depends(get_db) # DBセッションをDI
):
    
    # 1. 入力値（度）をラジアンに変換 (パラメータ)
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # 2. データベースのカラム（度）をラジアンに変換 (SQL func)
    # (モデルクラスを Communities と仮定)
    db_lat_rad = func.radians(Communities.latitude)
    db_lon_rad = func.radians(Communities.longitude)

    # 3. Haversine公式に基づき、SQLAlchemyで距離計算の式を構築
    delta_lat = db_lat_rad - lat_rad
    delta_lon = db_lon_rad - lon_rad

    a = func.pow(func.sin(delta_lat / 2), 2) + \
        func.cos(lat_rad) * func.cos(db_lat_rad) * \
        func.pow(func.sin(delta_lon / 2), 2)

    c = 2 * func.asin(func.sqrt(a))
    distance_km = EARTH_RADIUS_KM * c

    # 4. 構築した距離の式を使ってフィルタリング
    # (db.query(モデル) から始める)
    communities_result = db.query(Communities).filter(
        distance_km <= range
    ).all()
    
    return communities_result

# def calc_distance(lat1,lon1,lat2,lon2):
#     # この関数はSQLAlchemyの filter() では直接使えないため不要