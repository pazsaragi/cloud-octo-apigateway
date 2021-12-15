from app.models.user import CreateUserInput, User
from app.models.auth import TokenData
from app.settings import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from app.logger import get_logger
from app.database.user import UserDb
import uuid


class UserService:
    def __init__(self, db: UserDb = Depends()) -> None:
        self.db = db
        self.logger = get_logger("user-service")

    def get_user(self, email: str) -> User:
        user = self.db.get_user_by_email(email)
        return user

    async def get_current_user(self, token: str) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    async def create_user(self, user_input: CreateUserInput) -> User:
        try:
            self.logger.info(
                "LogReference=USERSERVICECREATEUSER, Message=Attempting Validation"
            )
            user = User(
                pk=str(uuid.uuid4()),
                sk=user_input.email,
                email=user_input.email,
                password=user_input.password,
            )
            self.logger.info(
                "LogReference=USERSERVICECREATEUSER, Message=Creating user"
            )
            return self.db.create(user)
        except Exception as e:
            self.logger.error(f"LogReference=USERSERVICECREATEUSER001, Error={e}")
            raise e
