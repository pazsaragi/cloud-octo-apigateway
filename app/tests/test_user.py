from fastapi.testclient import TestClient
from app.main import app
from app.tests.conftest import destroy_user_after_use

client = TestClient(app)


def test_create_user():
    test_email = "test@test.com"
    test_password = "secret"
    response = client.post(
        "/users/",
        json={"email": test_email, "password": test_password},
        headers={"content-type": "application/json"},
    )
    assert response.ok
    assert response.json()["Message"] is not None
    assert response.json()["user"] is not None
    response_body = response.json()["user"]

    destroy_user_after_use(response_body["pk"], response_body["sk"])


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
