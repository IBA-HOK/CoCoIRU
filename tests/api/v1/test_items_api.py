import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from db import models

# (conftest.py で client と db_session フィクスチャが自動的に読み込まれます)

def test_create_item(client: TestClient, db_session: Session):
    """
    [POST] /api/v1/items/ - 新しい品目の作成
    """
    response = client.post(
        "/api/v1/items/",
        json={
            "item_name": "Test Water", 
            "unit": "bottle", 
            "category": "drink",
            "description": "500ml"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item_name"] == "Test Water"
    assert data["unit"] == "bottle"
    assert "items_id" in data
    
    # DB側でも確認 (任意) - filter by name to avoid interference if other tests
    assert db_session.query(models.Items).filter(models.Items.item_name == "Test Water").count() == 1

def test_read_item(client: TestClient, db_session: Session):
    """
    [GET] /api/v1/items/{item_id} - 特定の品目の読み取り
    """
    # 先にデータを作成
    response_post = client.post(
        "/api/v1/items/",
        json={"item_name": "Test Food", "unit": "can", "category": "food"},
    )
    assert response_post.status_code == 200
    item_id = response_post.json()["items_id"]

    # 作成したデータをGET
    response_get = client.get(f"/api/v1/items/{item_id}")
    assert response_get.status_code == 200
    data = response_get.json()
    assert data["item_name"] == "Test Food"
    assert data["items_id"] == item_id

def test_read_item_not_found(client: TestClient):
    """
    [GET] /api/v1/items/{item_id} - 存在しない品目の読み取り (404)
    """
    response = client.get("/api/v1/items/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_read_items(client: TestClient):
    """
    [GET] /api/v1/items/ - 品目一覧の読み取り
    """
    # データを2つ作成
    client.post("/api/v1/items/", json={"item_name": "Item A", "unit": "pc"})
    client.post("/api/v1/items/", json={"item_name": "Item B", "unit": "box"})

    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # At least the two created items should be present; allow other items from
    # other tests to exist in the DB
    names = {d["item_name"] for d in data}
    assert "Item A" in names and "Item B" in names

def test_update_item(client: TestClient):
    """
    [PUT] /api/v1/items/{item_id} - 品目の更新
    """
    # 1. データ作成
    response_post = client.post(
        "/api/v1/items/",
        json={"item_name": "Original Name", "unit": "kg"},
    )
    item_id = response_post.json()["items_id"]

    # 2. データ更新 (PUT)
    response_put = client.put(
        f"/api/v1/items/{item_id}",
        json={"item_name": "Updated Name", "unit": "g", "description": "New Desc"},
    )
    assert response_put.status_code == 200
    data = response_put.json()
    assert data["item_name"] == "Updated Name"
    assert data["unit"] == "g"
    assert data["description"] == "New Desc"
    assert data["items_id"] == item_id

    # 3. GETで確認
    response_get = client.get(f"/api/v1/items/{item_id}")
    assert response_get.status_code == 200
    assert response_get.json()["item_name"] == "Updated Name"

def test_delete_item(client: TestClient):
    """
    [DELETE] /api/v1/items/{item_id} - 品目の削除
    """
    # 1. データ作成
    response_post = client.post(
        "/api/v1/items/",
        json={"item_name": "To Be Deleted", "unit": "pc"},
    )
    item_id = response_post.json()["items_id"]

    # 2. データ削除 (DELETE)
    response_del = client.delete(f"/api/v1/items/{item_id}")
    assert response_del.status_code == 200
    assert response_del.json()["item_name"] == "To Be Deleted"

    # 3. GETで確認 (404 Not Found)
    response_get = client.get(f"/api/v1/items/{item_id}")
    assert response_get.status_code == 404

    # 4. DELETE (存在しないID)
    response_del_404 = client.delete(f"/api/v1/items/{item_id}")
    assert response_del_404.status_code == 404