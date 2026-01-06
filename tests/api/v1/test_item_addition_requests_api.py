import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.security import require_token
from db import crud, schemas


def _override_token(role: str):
    def _fn():
        return {
            "sub": f"test-{role}",
            "role": role,
        }

    return _fn


def test_item_addition_requests_permissions(client: TestClient, db_session):
    """
    権限の確認:
      - create/update: community と gov が許可
      - read/delete: gov のみ許可
    テストは同一DBセッション内でロールを切り替えて検証する
    """

    # 1) community をDBに作成してから作成可能を検証
    comm = schemas.CommunitiesCreate(name="test-comm", password="pass", latitude=None, longitude=None, member_count=None, created_at=None, member_id=None)
    db_comm = crud.create_community(db_session, comm)

    app.dependency_overrides[require_token] = _override_token("community")
    payload = {
        "community_id": db_comm.community_id,
        "item_name": "Test Item",
        "item_unit": "pcs",
        "reason": "For testing",
        "timestamp": "2025-12-16T12:00:00+09:00",
    }
    resp = client.post("/api/v1/item_addition_requests/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["item_name"] == "Test Item"
    add_id = data["add_req_id"]

    # 2) community ではReadできない
    app.dependency_overrides[require_token] = _override_token("community")
    resp = client.get(f"/api/v1/item_addition_requests/{add_id}")
    assert resp.status_code == 403

    # 3) gov ではRead可能
    app.dependency_overrides[require_token] = _override_token("gov")
    resp = client.get(f"/api/v1/item_addition_requests/{add_id}")
    assert resp.status_code == 200
    assert resp.json()["add_req_id"] == add_id

    # 4) community で更新可能
    app.dependency_overrides[require_token] = _override_token("community")
    update_payload = payload.copy()
    update_payload["item_name"] = "Updated Item"
    resp = client.put(f"/api/v1/item_addition_requests/{add_id}", json=update_payload)
    assert resp.status_code == 200
    assert resp.json()["item_name"] == "Updated Item"

    # 5) community では削除できない
    app.dependency_overrides[require_token] = _override_token("community")
    resp = client.delete(f"/api/v1/item_addition_requests/{add_id}")
    assert resp.status_code == 403

    # 6) gov で削除可能
    app.dependency_overrides[require_token] = _override_token("gov")
    resp = client.delete(f"/api/v1/item_addition_requests/{add_id}")
    assert resp.status_code == 200

    # 7) 削除後は404
    resp = client.get(f"/api/v1/item_addition_requests/{add_id}")
    assert resp.status_code == 404
