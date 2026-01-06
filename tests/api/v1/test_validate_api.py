import pytest
from fastapi.testclient import TestClient

def test_validate_community_credentials_valid(client: TestClient):
    """
    [POST] /api/v1/validate/ - コミュニティの有効な認証情報を検証
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "community",
            "community_id": 1,  # テストデータに依存
            "password": "testpassword"  # テストデータに依存
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "valid" in data
    # 実際のテストデータに基づいてアサート

def test_validate_community_credentials_invalid(client: TestClient):
    """
    [POST] /api/v1/validate/ - コミュニティの無効な認証情報を検証
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "community",
            "community_id": 1,
            "password": "wrongpassword"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == False

def test_validate_gov_credentials_valid(client: TestClient):
    """
    [POST] /api/v1/validate/ - govの有効な認証情報を検証
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "gov",
            "username": "testuser",  # テストデータに依存
            "password": "testpassword"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "valid" in data

def test_validate_gov_credentials_invalid(client: TestClient):
    """
    [POST] /api/v1/validate/ - govの無効な認証情報を検証
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "gov",
            "username": "testuser",
            "password": "wrongpassword"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] == False

def test_validate_invalid_user_type(client: TestClient):
    """
    [POST] /api/v1/validate/ - 無効なuser_type
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "invalid",
            "password": "password"
        },
    )
    assert response.status_code == 400

def test_validate_missing_community_id(client: TestClient):
    """
    [POST] /api/v1/validate/ - community用にcommunity_idが欠けている
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "community",
            "password": "password"
        },
    )
    assert response.status_code == 400

def test_validate_missing_username(client: TestClient):
    """
    [POST] /api/v1/validate/ - gov用にusernameが欠けている
    """
    response = client.post(
        "/api/v1/validate/",
        json={
            "user_type": "gov",
            "password": "password"
        },
    )
    assert response.status_code == 400