from typing import Optional, List
from pydantic import BaseModel


class TokenData(BaseModel):
    email: Optional[str] = None
    scopes: List[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginInput(BaseModel):
    email: str
    password: str
