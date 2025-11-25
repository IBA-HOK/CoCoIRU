import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# (conftest.py で client と db_session フィクスチャが自動的に読み込まれます)

def test_e2e_create_support_request_flow(client: TestClient):
    """
    [E2E APIテスト]
    支援要請 (SupportRequest) を作成するまでの依存関係 (API) を
    すべて呼び出すフローテスト。
    """
    
    # === [前提] データのセットアップ ===
    # 依存関係の末端から順にPOSTで作成していく

    # 1. 特記事項 (SpecialNotes) を作成
    response_note = client.post(
        "/api/v1/special_notes/",
        json={"notes_content_json": "{\"allergy\": \"none\"}"}
    )
    assert response_note.status_code == 200
    note_id = response_note.json()["special_notes_id"]

    # 2. メンバー (Members) を作成
    response_member = client.post(
        "/api/v1/members/",
        json={"special_notes_id": note_id}
    )
    assert response_member.status_code == 200
    member_id = response_member.json()["member_id"]

    # 3. 品目 (Items) を作成
    response_item = client.post(
        "/api/v1/items/",
        json={"item_name": "E2E Water", "unit": "bottle"}
    )
    assert response_item.status_code == 200
    item_id = response_item.json()["items_id"]

    # 4. コミュニティ (Communities) を作成
    response_comm = client.post(
        "/api/v1/communities/",
        json={
            "name": "E2E Test Community",
            "member_id": member_id,
            "member_count": 10,
            "password": "E2E-Pass-123",
        }
    )
    assert response_comm.status_code == 200
    community_id = response_comm.json()["community_id"]

    # === [実行] 支援要請の作成 ===

    # 5. 要請内容 (RequestContent) を作成 (水, 100個)
    response_content = client.post(
        "/api/v1/request_content/",
        json={"items_id": item_id, "number": 100, "other_note": "API Test"}
    )
    assert response_content.status_code == 200
    content_id = response_content.json()["request_content_id"]

    # 6. 支援要請 (SupportRequest) を作成
    response_req = client.post(
        "/api/v1/support_requests/",
        json={
            "community_id": community_id,
            "request_content_id": content_id,
            "status": "pending"
        }
    )
    assert response_req.status_code == 200
    data = response_req.json()
    
    # === [検証] ===
    assert data["community_id"] == community_id
    assert data["request_content_id"] == content_id
    assert data["status"] == "pending"
    assert "request_id" in data
    
    request_id = data["request_id"]
    
    # GETで要請を再取得して確認
    response_get = client.get(f"/api/v1/support_requests/{request_id}")
    assert response_get.status_code == 200
    assert response_get.json()["status"] == "pending"

def test_create_support_request_fk_violation(client: TestClient):
    """
    [整合性テスト]
    Support_Request APIが、存在しない外部キーで登録しようとした場合
    (DBレベルでのエラーをFastAPIがどうハンドルするか)
    
    注: SQLAlchemyはDBエラー (IntegrityError) を発生させ、
    FastAPIのデフォルトでは 500 Internal Server Error になります。
    (これを4xx系にしたい場合は、カスタム例外ハンドラが必要です)
    """
    
    # 存在しないID (999) を使う
    response = client.post(
        "/api/v1/support_requests/",
        json={
            "community_id": 999,
            "request_content_id": 999,
            "status": "failed_fk"
        }
    )
    
    # デフォルトの例外処理では 4090 が返る
    assert response.status_code == 409
    
    # (もしPydanticのバリデーションでチェックするなら 422 Unprocessable Entity)
    # (もしカスタム例外ハンドラで 404 にマップするなら 404 Not Found)