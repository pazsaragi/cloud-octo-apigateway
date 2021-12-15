import boto3
from abc import ABC, abstractmethod
from app.settings import LOCALSTACK_HOSTNAME


class BaseDatabase(ABC):
    """
    Base class for database implementation.
    """

    pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def query(self):
        pass


class DynamoDB(BaseDatabase):
    def __init__(self, table_name: str) -> None:
        super().__init__()
        if LOCALSTACK_HOSTNAME:
            dynamodb_endpoint = "http://%s:4566" % LOCALSTACK_HOSTNAME
            print(dynamodb_endpoint)
            self._dynamodb = boto3.client("dynamodb", endpoint_url=dynamodb_endpoint)
            print(self._dynamodb.list_tables())
        else:
            self._dynamodb = boto3.client("dynamodb")
        self._table = table_name

    def get_table(self):
        return self._table

    def get_client(self):
        return self._dynamodb

    def create(self, data):
        """
        DynamoDB put item.
        """
        print(data, self.get_table())
        return self._dynamodb.put_item(
            TableName=self.get_table(),
            Item={"pk": {"S": "h"}, "sk": {"S": "h"}, "email": {"S": "h"}},
        )

    def get(self, key, value):
        """
        DynamoDB get item.
        """
        return self._table.get_item(Key={key: value})

    def query(self):
        return super().query()
