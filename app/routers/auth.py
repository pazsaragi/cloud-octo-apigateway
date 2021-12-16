from datetime import timedelta
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.auth import LoginInput, Token
from app.services.auth import AuthService
from app.logger import get_logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

logger = get_logger("auth-router")

# class AuthHandler:
#     def __init__(self) -> None:
#         pass

#     def authenticate_user(
#         self, username: str, password: str, repo=Depends(get_auth_service())
#     ) -> User:
#         return repo.authenticate_user(username, password)


# def get_auth_handler(handler=Depends(AuthHandler)) -> AuthHandler:
#     return handler


@router.post("/token", response_model=Token)
async def login_for_access_token(data: LoginInput, service: AuthService = Depends()):
    try:
        user = service.authenticate_user(data.email, data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"LogReference=AUTH-ROUTER-TOKEN-0001, Error={e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
