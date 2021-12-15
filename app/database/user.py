from app.models.user import CreateUserInput, GetUserInput, User
from app.settings import AUTH_TABLE_NAME
from .db import DynamoDB
from fastapi import Depends
import uuid
from boto3.dynamodb.conditions import Key
from app.logger import get_logger


class UserDb(DynamoDB):
    def __init__(self) -> None:
        super().__init__(table_name=AUTH_TABLE_NAME)
        self.logger = get_logger("user-db")

    def create(self, user: User) -> User:
        """
        Creates a new user.

        :param user_input:
        """
        try:
            return super().create(user.json())
        except Exception as e:
            self.logger.error(f"LogReference=USERSERVCE00C1, Error={e}")
            raise e

    def get_user_by_email(self, email: str) -> User:
        """
        Queries user by email-index.

        :param email:
        """
        user = self.get_table().query(
            IndexName="email-index", KeyConditionExpression=Key("email").eq(email)
        )
        return user

    def get(self, user_input: GetUserInput) -> User:
        """
        Queries user by email-index.
        """
        pass


def get_db(db: DynamoDB = Depends(UserDb)):
    return db
