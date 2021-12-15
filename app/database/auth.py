from app.models.user import CreateUserInput, User
from app.settings import AUTH_TABLE_NAME
from .db import DynamoDB
from fastapi import Depends


class AuthDb(DynamoDB):
    def __init__(self) -> None:
        super().__init__(table_name=AUTH_TABLE_NAME)

    def create(self, user_input: CreateUserInput) -> User:
        print(user_input)

    def query(self, email: str) -> User:
        """
        Queries user by email-index.
        """
        print(email)


def get_auth_db(db: DynamoDB = Depends(AuthDb)):
    return db
