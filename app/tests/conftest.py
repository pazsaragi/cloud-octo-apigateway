import os
import pytest
import json

os.environ[
    "SECRET_KEY"
] = "420455e83acce77c7f26b1cd32da91be9884a9b27426af6daeb65cd8e693e603"
os.environ["ALLOWED_HOSTS"] = json.dumps(["*"])


@pytest.fixture()
def get_token():
    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.post(
        "/auth/token",
        json={"username": "johndoe", "password": "secret"},
        headers={"content-type": "application/json"},
    )
    yield response.json()["access_token"]
