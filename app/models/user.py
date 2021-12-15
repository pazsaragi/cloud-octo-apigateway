from pydantic import BaseModel
from typing import List, Optional


class Role(BaseModel):
    name: str
    description: Optional[str] = None


class User(BaseModel):
    pk: str
    sk: str
    email: str
    password: str


class CreateUserInput(BaseModel):
    email: str
    password: str


class GetUserInput(BaseModel):
    pk: str
    email: str
