from fastapi import APIRouter

from app.schemas.user import User, UserCreate, UserRead, UserUpdate
from app.users import fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/users", tags=["users"]
)
router.include_router(
    fastapi_users.get_users_router(User, UserUpdate), prefix="/users", tags=["users"]
)