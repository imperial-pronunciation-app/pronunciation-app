from types import TracebackType
from typing import AsyncContextManager, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.attempts_repository import AttemptRepository
from app.crud.exercise_repository import ExerciseRepository
from app.crud.leaderboard_user_repository import LeaderboardUserRepository
from app.crud.lesson_repository import LessonRepository
from app.crud.phoneme_repository import PhonemeRepository
from app.crud.recording_repository import RecordingRepository
from app.crud.unit_repository import UnitRepository
from app.crud.user_repository import UserRepository
from app.crud.word_repository import WordRepository
from app.database import get_async_session


class UnitOfWork(AsyncContextManager["UnitOfWork"]):
    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        self._session = session
        self.recordings = RecordingRepository(self._session)
        self.leaderboard_users = LeaderboardUserRepository(self._session)
        self.words = WordRepository(self._session)
        self.phonemes = PhonemeRepository(self._session)
        self.users = UserRepository(self._session)
        self.exercises = ExerciseRepository(self._session)
        self.units = UnitRepository(self._session)
        self.lessons = LessonRepository(self._session)
        self.attempts = AttemptRepository(self._session)
    
    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        type_: type[BaseException] | None,
        value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.rollback()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


async def get_unit_of_work(session: AsyncSession = Depends(get_async_session)) -> AsyncIterator[UnitOfWork]:
    async with UnitOfWork(session) as uow:
        yield uow
