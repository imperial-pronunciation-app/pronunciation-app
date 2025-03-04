from fastapi import APIRouter

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.users import fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_register_router(User, UserCreate), prefix="/users", tags=["users"]
)
router.include_router(
    fastapi_users.get_users_router(User, UserUpdate), prefix="/users", tags=["users"]
)
