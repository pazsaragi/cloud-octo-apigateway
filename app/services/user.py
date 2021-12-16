from app.models.user import CreateUserInput, DeleteUserInput, User
from app.models.auth import TokenData
from app.services.auth import AuthService
from app.settings import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from app.logger import get_logger
from app.database.user import UserDb
import uuid


class UserService:
    def __init__(
        self, db: UserDb = Depends(), auth_svc: AuthService = Depends()
    ) -> None:
        self.db = db
        self.logger = get_logger("user-service")
        self.auth_svc = auth_svc

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
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        user = self.get_user(email=token_data.email)
        if user is None:
            raise credentials_exception
        return user

    async def create_user(self, user_input: CreateUserInput) -> User:
        try:
            self.logger.info(
                "LogReference=USER-SERVICE-CREATEUSER, Message=Attempting Validation"
            )
            user = User(
                pk=f"USER#{str(uuid.uuid4())}",
                sk=user_input.email,
                email=user_input.email,
                password=self.auth_svc.get_password_hash(user_input.password),
            )
            self.logger.info(
                "LogReference=USER-SERVICE-CREATEUSER, Message=Creating user"
            )
            self.db.create(
                {
                    "pk": user.pk,
                    "sk": user.sk,
                    "email": user.email,
                    "password": user.password,
                }
            )

            user.password = None

            return user
        except Exception as e:
            self.logger.error(f"LogReference=USER-SERVICE-CREATEUSER, Error={e}")
            raise e

    async def delete_user(self, user_input: DeleteUserInput) -> bool:
        try:
            self.logger.info(
                "LogReference=USER-SERVICE-DELETEUSER-0001, Message=Attempting Validation"
            )
            user = self.get_user(email=user_input.sk)
            if user is None:
                raise Exception("User not found")
            self.logger.info(
                "LogReference=USER-SERVICE-DELETEUSER-0002, Message=Deleting user"
            )
            self.db.delete("pk", user.pk, "sk", user.sk)
            return True
        except Exception as e:
            self.logger.error(f"LogReference=USER-SERVICE-DELETEUSER-0003, Error={e}")
            raise e
