from sqlmodel import Session, col

from app.crud.generic_repository import GenericRepository
from app.models.unit import Unit


class UnitRepository(GenericRepository[Unit]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Unit)

    def all_ordered(self) -> list[Unit]:
        return self._session.query(Unit).order_by(col(Unit.index)).all()
    
