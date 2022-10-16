"""User managements endpoints."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.schemas import UserCreate, UserRead, UserUpdate
from src.users import auth_backend, current_active_user, fastapi_users
from fastapi import Depends
from src.db import User

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
user_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
user_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@user_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """Endpoint to test if authentication works."""
    return {"message": f"Hello {user.email}!"}
