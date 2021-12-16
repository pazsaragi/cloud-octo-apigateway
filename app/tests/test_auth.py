from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_token(create_and_destroy_user):
    _, email, password = create_and_destroy_user
    response = client.post(
        "/auth/token",
        json={"email": email, "password": password},
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"


def test_user():
    response = client.get("/users/me")
    assert response.status_code == 401
