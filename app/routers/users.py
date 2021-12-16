from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header
from app.models.user import CreateUserInput, User
from app.services.user import UserService
from app.logger import get_logger

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)
logger = get_logger("users-router")


@router.get("/me/", response_model=User)
async def read_users_me(
    authorization: Optional[str] = Header(None), user_service: UserService = Depends()
):
    try:
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        bearer_token = authorization.split(" ")[1]
        user = await user_service.get_current_user(bearer_token)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"LogReference=USERS-ROUTER-GET-ME-0001, Error={e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me/items/")
async def read_own_items(user_service: UserService = Depends()):
    user = user_service.get_current_user()
    return [{"item_id": "Foo", "owner": user.email}]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(data: CreateUserInput, user_service: UserService = Depends()):
    try:
        user = user_service.get_user(email=data.email)
        if user:
            logger.info("LogReference=CREATE-USER-ROUTER-0003, Message=User exists.")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists",
            )
        logger.info(
            "LogReference=CREATE-USER-ROUTER-0002, Message=No user exists. Creating user"
        )
        user = await user_service.create_user(data)
        return {"Message": "User Created", "user": user}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"LogReference=CREATE-USER-ROUTER-0001, Error creating user: {e}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create user",
        )
