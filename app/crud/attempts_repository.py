from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.attempt import Attempt


class AttemptRepository(GenericRepository[Attempt]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Attempt)

    async def find_by_user_id_and_exercise_id(self, user_id: int, exercise_id: int) -> Sequence[Attempt]:
        stmt = (
            select(Attempt)
            .where(Attempt.user_id == user_id, Attempt.exercise_id == exercise_id)
        )
        return (await self._session.execute(stmt)).scalars().all()
