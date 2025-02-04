from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.exercise import Attempt


class AttemptRepository(GenericRepository[Attempt]):

    def __init__(self, session: Session):
        super().__init__(session, Attempt)

    