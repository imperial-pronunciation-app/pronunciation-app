from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.user import User


class UserRepository(GenericRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def get_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)  # type: ignore
        return (await self._session.execute(stmt)).scalar_one()

    async def find_by_new_users_created_before(self, created_before: date) -> Sequence[User]:
        stmt = select(User).where(User.new_user).where(User.created_at < created_before)
        return (await self._session.execute(stmt)).scalars().all()
