from typing import Generic, List, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.id_model import IdModel


T = TypeVar("T", bound=IdModel)

class GenericRepository(Generic[T]):

    def __init__(self, session: AsyncSession, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    async def get_by_id(self, id: int) -> T:
        return await self._session.get_one(self._model_cls, id)
    
    async def get_by_ids(self, ids: List[int]) -> Sequence[T]:
        stmt = select(self._model_cls).where(self._model_cls.id.in_(ids))
        return (await self._session.execute(stmt)).scalars().all()
    
    async def find_by_id(self, id: int) -> Optional[T]:
        return await self._session.get(self._model_cls, id)
    
    async def all(self) -> Sequence[T]:
        stmt = select(self._model_cls)
        return (await self._session.execute(stmt)).scalars().all()

    async def upsert(self, record: T) -> T:
        self._session.add(record)
        await self._session.flush()
        await self._session.refresh(record)
        return record

    async def upsert_all(self, records: Sequence[T]) -> Sequence[T]:
        self._session.add_all(records)
        await self._session.flush()
        for record in records:
            await self._session.refresh(record)
        return records

    async def delete(self, id: int) -> None:
        record = await self.find_by_id(id)
        if record:
            await self._session.delete(record)
            await self._session.flush()
