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
            self._dynamodb = boto3.resource("dynamodb", endpoint_url=dynamodb_endpoint)
        else:
            self._dynamodb = boto3.resource("dynamodb")
        self._table = self._dynamodb.Table(table_name)

    def get_table(self):
        return self._table

    def get_client(self):
        return self._dynamodb

    def create(self, data):
        """
        DynamoDB put item.

        Expects data to be json serialized.
        """
        return self.get_table().put_item(
            Item=data,
        )

    def get(self, key, value):
        """
        DynamoDB get item.
        """
        return self.get_table().get_item(Key={key: value})

    def query(self):
        return super().query()

    def delete(self, pk_key, pk_value, sk_key, sk_value):
        """
        DynamoDB delete item.
        """
        return self.get_table().delete_item(Key={pk_key: pk_value, sk_key: sk_value})
