from typing import Generic, List, Optional, Sequence, Type, TypeVar

from sqlmodel import Session, select

from app.models.id_model import IdModel


T = TypeVar("T", bound=IdModel)

class GenericRepository(Generic[T]):

    def __init__(self, session: Session, model_cls: Type[T]) -> None:
        self._session = session
        self._model_cls = model_cls

    def get_by_id(self, id: int) -> T:
        return self._session.get_one(self._model_cls, id)
    
    def get_by_ids(self, ids: List[int]) -> List[T]:
        return [self.get_by_id(id) for id in ids]
    
    def find_by_id(self, id: int) -> Optional[T]:
        return self._session.get(self._model_cls, id)
    
    def all(self) -> Sequence[T]:
        stmt = select(self._model_cls)
        return self._session.exec(stmt).all()

    def upsert(self, record: T) -> T:
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return record

    def upsert_all(self, records: Sequence[T]) -> Sequence[T]:
        self._session.add_all(records)
        self._session.flush()
        for record in records:
            self._session.refresh(record)
        return records

    def delete(self, id: int) -> None:
        record = self.find_by_id(id)
        if record:
            self._session.delete(record)
            self._session.flush()
