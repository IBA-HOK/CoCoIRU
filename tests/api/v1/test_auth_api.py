from fastapi.testclient import TestClient


def test_issue_token_success(client: TestClient):
    response = client.post(
        "/api/v1/token",
        json={"username": "admin", "password": "admin"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0
    assert isinstance(data["access_token"], str) and data["access_token"]


def test_issue_token_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/v1/token",
        json={"username": "admin", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
