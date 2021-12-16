import pytest
import asyncio
from app.database.user import UserDb
from app.main import app
from fastapi.testclient import TestClient
from app.models.user import CreateUserInput, DeleteUserInput
from app.services.auth import AuthService
from app.services.user import UserService

client = TestClient(app)
auth_svc = AuthService()
db = UserDb()
user_svc = UserService(db, auth_svc)


@pytest.fixture()
def get_token(create_and_destroy_user):
    _, email, password = create_and_destroy_user
    response = client.post(
        "/auth/token",
        json={"email": email, "password": password},
        headers={"content-type": "application/json"},
    )
    yield response.json()["access_token"]


@pytest.fixture()
def create_test_user():
    test_email = "test@test.com"
    test_password = "secret"
    user = CreateUserInput(
        email=test_email,
        password=test_password,
    )
    user = asyncio.run(user_svc.create_user(user))

    yield user.pk, test_email, test_password


@pytest.fixture()
def create_and_destroy_user(create_test_user):
    pk, test_email, test_password = create_test_user

    yield pk, test_email, test_password

    destroy_user_after_use(pk, test_email)


def destroy_user_after_use(pk, sk):
    delete_user_input = DeleteUserInput(pk=pk, sk=sk)
    user_svc.delete_user(delete_user_input)
