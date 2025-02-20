from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.word import Word


class WordRepository(GenericRepository[Word]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Word)
