from fastapi import APIRouter

from app.users import auth_backend, fastapi_users


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)