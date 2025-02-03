from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.word import Word


class WordRepository(GenericRepository[Word]):

    def __init__(self, session: Session):
        super().__init__(session, Word)
