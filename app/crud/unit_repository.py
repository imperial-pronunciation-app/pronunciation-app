from typing import Sequence

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.unit import Unit


class UnitRepository(GenericRepository[Unit]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Unit)
    
    def for_language(self, language_id: int) -> Sequence[Unit]:
        return self._session.exec(select(Unit).where(Unit.language_id == language_id)).all()
    
