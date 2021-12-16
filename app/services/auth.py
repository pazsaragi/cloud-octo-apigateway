from app.models.user import CreateUserInput, User
from app.database.user import UserDb
from app.settings import SECRET_KEY, ALGORITHM
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta
from app.dependencies import pwd_context
from fastapi import Depends
from app.logger import get_logger


class AuthService:
    def __init__(self, db: UserDb = Depends()) -> None:
        self.db = db
        self.logger = get_logger("auth-service")

    def create_user(self, user_input: CreateUserInput) -> User:
        try:
            user = self.db.create(user_input)
            return user
        except Exception as e:
            self.logger.error(f"LogReference=AUTHSERVICE00C1, Error: {e}")

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        """
        Encodes a JWT to be used for authentication.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        """
        Bcrypt compare between plain text password and hashed password.
        """
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            print(e)
            return False

    def get_password_hash(self, password):
        """
        Hashes a plain text password.
        """
        try:
            return pwd_context.hash(password)
        except Exception as e:
            self.logger.error(f"LogReference=AUTHSERVICE00PW2, Error: {e}")

    def authenticate_user(self, email: str, password: str) -> User or bool:
        user = self.db.get_user_by_email(email)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user


def get_auth_service(repo=Depends(AuthService)):
    return repo
