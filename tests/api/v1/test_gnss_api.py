import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from db import models
import math

# (conftest.py で client と db_session フィクスチャが自動的に読み込まれます)

def haversine_km(lat1, lon1, lat2, lon2):
    """
    Python側で2点間の距離（km）を計算するヘルパー関数
    テストで期待値を検証するために使用
    """
    R = 6371.0  # 地球の半径 (km)
    rlat1, rlon1, rlat2, rlon2 = map(math.radians, (lat1, lon1, lat2, lon2))
    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1
    a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(min(1, math.sqrt(a)))
    return R * c


def test_nearby_returns_communities_within_range(client: TestClient, db_session: Session):
    """
    [GET] /api/v1/gnss/nearby - 範囲内のコミュニティが正しく返されることを確認
    """
    # 基準点: 東京駅付近 (35.681236, 139.767125)
    base_lat = 35.681236
    base_lon = 139.767125
    search_range_km = 5.0

    # テスト用コミュニティを複数作成
    # 範囲内のコミュニティ（約2km離れた位置）
    community_near = models.Communities(
        community_id=None,
        name="Near Community",
        latitude=35.7,  # 約2km北
        longitude=139.767,
        member_id=None,
        member_count=0,
        created_at="2025-01-01T00:00:00"
    )
    db_session.add(community_near)
    
    # 範囲外のコミュニティ（約50km離れた位置）
    community_far = models.Communities(
        community_id=None,
        name="Far Community",
        latitude=36.1,  # 約50km北
        longitude=139.767,
        member_id=None,
        member_count=0,
        created_at="2025-01-01T00:00:00"
    )
    db_session.add(community_far)
    
    # 別の範囲内コミュニティ（約4km）
    community_near2 = models.Communities(
        community_id=None,
        name="Near Community 2",
        latitude=35.64,  # 約4.5km南
        longitude=139.767,
        member_id=None,
        member_count=0,
        created_at="2025-01-01T00:00:00"
    )
    db_session.add(community_near2)
    
    db_session.commit()

    # API呼び出し
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": base_lat,
            "longitude": base_lon,
            "range": search_range_km
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # 返されたコミュニティ名を確認
    returned_names = {c["name"] for c in data}
    
    # 範囲内のコミュニティが含まれていることを確認
    assert "Near Community" in returned_names
    assert "Near Community 2" in returned_names
    
    # 範囲外のコミュニティが含まれていないことを確認
    assert "Far Community" not in returned_names
    
    # 全ての返されたコミュニティが範囲内であることを再確認
    for c in data:
        dist = haversine_km(base_lat, base_lon, c["latitude"], c["longitude"])
        assert dist <= search_range_km, f"Community {c['name']} is {dist}km away, exceeds range {search_range_km}km"


def test_nearby_empty_result_when_no_communities_in_range(client: TestClient, db_session: Session):
    """
    [GET] /api/v1/gnss/nearby - 範囲内にコミュニティがない場合、空のリストが返されることを確認
    """
    # 遠く離れた場所にコミュニティを作成（札幌付近: 43.064, 141.347）
    community_sapporo = models.Communities(
        community_id=None,
        name="Sapporo Community",
        latitude=43.064,
        longitude=141.347,
        member_id=None,
        member_count=0,
        created_at="2025-01-01T00:00:00"
    )
    db_session.add(community_sapporo)
    db_session.commit()
    
    # 東京駅付近で5km範囲内を検索（札幌は約800km離れている）
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681236,
            "longitude": 139.767125,
            "range": 5.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # 範囲内にコミュニティがないので空のリスト


def test_nearby_validation_latitude_out_of_range(client: TestClient):
    """
    [GET] /api/v1/gnss/nearby - 緯度が範囲外の場合、422エラーが返されることを確認
    """
    # 緯度が180を超える
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 200.0,
            "longitude": 139.767,
            "range": 5.0
        }
    )
    assert response.status_code == 422
    
    # 緯度が-180を下回る
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": -200.0,
            "longitude": 139.767,
            "range": 5.0
        }
    )
    assert response.status_code == 422


def test_nearby_validation_longitude_out_of_range(client: TestClient):
    """
    [GET] /api/v1/gnss/nearby - 経度が範囲外の場合、422エラーが返されることを確認
    """
    # 経度が180を超える
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681,
            "longitude": 200.0,
            "range": 5.0
        }
    )
    assert response.status_code == 422
    
    # 経度が-180を下回る
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681,
            "longitude": -200.0,
            "range": 5.0
        }
    )
    assert response.status_code == 422


def test_nearby_validation_range_must_be_positive(client: TestClient):
    """
    [GET] /api/v1/gnss/nearby - rangeが0以下の場合、422エラーが返されることを確認
    """
    # range = 0
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681,
            "longitude": 139.767,
            "range": 0.0
        }
    )
    assert response.status_code == 422
    
    # range < 0
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681,
            "longitude": 139.767,
            "range": -5.0
        }
    )
    assert response.status_code == 422


def test_nearby_validation_missing_parameters(client: TestClient):
    """
    [GET] /api/v1/gnss/nearby - 必須パラメータが欠けている場合、422エラーが返されることを確認
    """
    # latitudeが欠けている
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "longitude": 139.767,
            "range": 5.0
        }
    )
    assert response.status_code == 422
    
    # longitudeが欠けている
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681,
            "range": 5.0
        }
    )
    assert response.status_code == 422
    
    # rangeが欠けている
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": 35.681,
            "longitude": 139.767
        }
    )
    assert response.status_code == 422


def test_nearby_with_multiple_communities_various_distances(client: TestClient, db_session: Session):
    """
    [GET] /api/v1/gnss/nearby - 複数のコミュニティを様々な距離に配置して正確にフィルタされることを確認
    """
    base_lat = 35.0
    base_lon = 135.0
    search_range_km = 10.0
    
    # 複数のコミュニティをランダムな距離に配置
    test_communities = [
        # (name, lat_offset_degrees, lon_offset_degrees, expected_distance_km_approx)
        ("Very Close", 0.01, 0.01, 1.4),   # 約1.4km - 範囲内
        ("Close", 0.05, 0.05, 7.0),        # 約7km - 範囲内
        ("At Edge", 0.09, 0.0, 10.0),      # 約10km - 範囲内（境界）
        ("Just Outside", 0.1, 0.0, 11.1),  # 約11km - 範囲外
        ("Far Away", 0.5, 0.5, 70.0),      # 約70km - 範囲外
    ]
    
    for name, lat_offset, lon_offset, _ in test_communities:
        community = models.Communities(
            community_id=None,
            name=name,
            latitude=base_lat + lat_offset,
            longitude=base_lon + lon_offset,
            member_id=None,
            member_count=0,
            created_at="2025-01-01T00:00:00"
        )
        db_session.add(community)
    
    db_session.commit()
    
    # API呼び出し
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": base_lat,
            "longitude": base_lon,
            "range": search_range_km
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # 各コミュニティの距離を実際に計算して検証
    returned_names = {c["name"] for c in data}
    
    for name, lat_offset, lon_offset, expected_dist in test_communities:
        actual_dist = haversine_km(base_lat, base_lon, base_lat + lat_offset, base_lon + lon_offset)
        
        if actual_dist <= search_range_km:
            assert name in returned_names, f"{name} (distance: {actual_dist:.2f}km) should be included"
        else:
            assert name not in returned_names, f"{name} (distance: {actual_dist:.2f}km) should be excluded"


def test_nearby_handles_communities_with_exact_same_location(client: TestClient, db_session: Session):
    """
    [GET] /api/v1/gnss/nearby - 基準点と全く同じ座標のコミュニティが正しく返されることを確認
    """
    base_lat = 40.0
    base_lon = 140.0
    
    # 基準点と全く同じ位置のコミュニティ
    community_same = models.Communities(
        community_id=None,
        name="Same Location",
        latitude=base_lat,
        longitude=base_lon,
        member_id=None,
        member_count=0,
        created_at="2025-01-01T00:00:00"
    )
    db_session.add(community_same)
    db_session.commit()
    
    response = client.get(
        "/api/v1/gnss/nearby",
        params={
            "latitude": base_lat,
            "longitude": base_lon,
            "range": 1.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Same Location"
    
    # 距離は0であるべき
    dist = haversine_km(base_lat, base_lon, data[0]["latitude"], data[0]["longitude"])
    assert dist < 0.01  # ほぼ0km
