from app.models.user import CreateUserInput, GetUserInput, User
from app.settings import AUTH_TABLE_NAME
from .db import DynamoDB
from fastapi import Depends
from boto3.dynamodb.conditions import Key
from app.logger import get_logger


class UserDb(DynamoDB):
    def __init__(self) -> None:
        super().__init__(table_name=AUTH_TABLE_NAME)
        self.logger = get_logger("user-db")

    def create(self, user: dict) -> User:
        """
        Creates a new user.

        :param user_input:
        """
        try:
            return super().create(user)
        except Exception as e:
            self.logger.error(f"LogReference=USER-DB-0001, Error={e}")
            raise e

    def get_user_by_email(self, email: str) -> User:
        """
        Queries user by email-index.

        :param email:
        """
        try:
            user = self.get_table().query(
                IndexName="email-index",
                KeyConditionExpression=Key("email").eq(f"{email}")
                & Key("pk").begins_with("USER#"),
            )
            if "Count" in user and user["Count"] == 0:
                return None
            return User(**user["Items"][0])
        except Exception as e:
            self.logger.error(f"LogReference=USER-DB-0002, Error={e}")
            raise e

    def get(self, user_input: GetUserInput) -> User:
        """
        Queries user by email-index.
        """
        pass

    def delete_user(self, pk: str, sk: str) -> None:
        """
        Delete's a user by email.
        """
        super().delete("pk", pk, "sk", sk)
        return


def get_db(db: DynamoDB = Depends(UserDb)):
    return db
