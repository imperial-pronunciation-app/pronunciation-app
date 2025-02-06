
from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.exercise import Exercise


class ExerciseRepository(GenericRepository[Exercise]):

    def __init__(self, session: Session):
        super().__init__(session, Exercise)

    