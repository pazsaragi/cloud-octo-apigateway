from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_me(get_token):
    token = get_token
    response = client.get(
        "/users/me/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


def test_unauthorized():
    response = client.get("/users/me/")
    assert response.status_code == 401


def test_get_items(get_token):
    token = get_token
    response = client.get(
        "/users/me/items/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
