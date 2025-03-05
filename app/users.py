from typing import AsyncGenerator, Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlmodel import SQLModelUserDatabase

from app.config import get_settings
from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.database import get_user_db
from app.models.leaderboard_user_link import LeaderboardUserLink
from app.models.user import User
from app.redis import LRedis
from app.services.user import UserService


secret = get_settings().USER_MANAGER_SECRET

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = secret
    verification_token_secret = secret

    def __init__(self, user_db: SQLModelUserDatabase, uow: UnitOfWork) -> None:
        self._uow = uow
        super().__init__(user_db)

    async def on_after_register(self, user: User, request: Optional[Request] = None) -> None:
        # Set default language for user
        user.language_id = self._uow.languages.get_default().id
        self._uow.users.upsert(user)
        self._uow.commit()

        # Create leaderboard entry
        leaderboard_user = self._uow.leaderboard_users.upsert(LeaderboardUserLink(user_id=user.id)) # Defaults to bronze league and 0 xp
        self._uow.commit()
        LRedis.create_entry_from_user(leaderboard_user)

    async def on_after_login(self, user: User, request: Optional[Request] = None, response: Optional[Response] = None) -> None:
        user_service = UserService(self._uow)
        user_service.update_login_streak(user)


async def get_user_manager(user_db: SQLModelUserDatabase = Depends(get_user_db), uow: UnitOfWork = Depends(get_unit_of_work)) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db, uow)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
