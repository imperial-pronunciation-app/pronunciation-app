from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.unit import Unit


class UnitRepository(GenericRepository[Unit]):

    def __init__(self, session: Session) -> None:
        super().__init__(session, Unit)
    
