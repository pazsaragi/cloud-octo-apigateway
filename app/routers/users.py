from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import CreateUserInput, User
from app.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/me/", response_model=User)
async def read_users_me(user_service: UserService = Depends()):
    user = user_service.get_current_user()
    return user


@router.get("/me/items/")
async def read_own_items(user_service: UserService = Depends()):
    user = user_service.get_current_user()
    return [{"item_id": "Foo", "owner": user.email}]


@router.post("/")
async def create(data: CreateUserInput, user_service: UserService = Depends()):
    # user = user_service.get_user(email=data.email)
    # if user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="A user with this email already exists",
    #     )
    try:
        print("Creating User", data.dict())
        await user_service.create_user(data)
        return {"Message": "User Created"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create user",
        )
