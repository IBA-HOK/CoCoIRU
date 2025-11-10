from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import math
import logging

from db.session import get_db
from db.models import Communities
from db import schemas

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

# 地球の半径 (km)
EARTH_RADIUS_KM = 6371.0

@router.get("/nearby", response_model=List[schemas.Communities]) # スキーマを指定
async def get_locations(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Latitude in degrees between -90 and 90"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Longitude in degrees between -180 and 180"),
    range_km: float = Query(..., gt=0.0, alias="range", description="Search radius in km; must be positive"),
    db: Session = Depends(get_db) # DBセッションをDI
):
    
    # 1. 入力値（度）をラジアンに変換 (パラメータ)
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # NOTE:
    # SQLite (used in tests) does not provide trig functions like
    # SIN/COS/ASIN/RADIANS by default. To keep compatibility we:
    # 1) compute a bounding box (degrees) that certainly contains points
    #    within the requested radius, 2) query the DB for that box, and
    # 3) compute the exact Haversine distance in Python and filter.

    # Bounding box (in degrees)
    # delta_lat = range_km / R (radians) -> convert to degrees
    delta_lat_deg = (range_km / EARTH_RADIUS_KM) * (180.0 / math.pi)
    # delta_lon depends on latitude
    # protect against cos(lat) == 0 near poles
    cos_lat = math.cos(lat_rad)
    if abs(cos_lat) < 1e-9:
        # at poles, longitude span is effectively 180 degrees
        delta_lon_deg = 180.0
    else:
        delta_lon_deg = delta_lat_deg / cos_lat

    def clamp_lat(lat):
        return max(-90.0, min(90.0, lat))

    def wrap_lon(lon):
        # Wrap longitude to [-180, 180]
        return ((lon + 180.0) % 360.0) - 180.0

    min_lat = clamp_lat(latitude - delta_lat_deg)
    max_lat = clamp_lat(latitude + delta_lat_deg)
    min_lon = wrap_lon(longitude - delta_lon_deg)
    max_lon = wrap_lon(longitude + delta_lon_deg)
    candidates = db.query(Communities).filter(
        Communities.latitude.between(min_lat, max_lat),
        Communities.longitude.between(min_lon, max_lon)
    ).all()

    def haversine_km(lat1, lon1, lat2, lon2):
        # returns distance in kilometers
        rlat1, rlon1, rlat2, rlon2 = map(math.radians, (lat1, lon1, lat2, lon2))
        dlat = rlat2 - rlat1
        dlon = rlon2 - rlon1
        a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(min(1, math.sqrt(a)))
        return EARTH_RADIUS_KM * c

    communities_result = []
    for c in candidates:
        try:
            comm_lat = float(c.latitude)
            comm_lon = float(c.longitude)
        except (ValueError, TypeError, AttributeError) as e:
            # skip records with invalid coordinates and log the error
            logger.warning(
                f"Skipping community {c.community_id} due to invalid coordinates. "
                f"Error type: {type(e).__name__}"
            )
            continue
        dist = haversine_km(latitude, longitude, comm_lat, comm_lon)
        if dist <= range_km:
            communities_result.append(c)

    return communities_result
