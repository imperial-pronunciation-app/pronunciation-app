
from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.language import Language


class LanguageRepository(GenericRepository[Language]):

    def __init__(self, session: Session):
        super().__init__(session, Language)

    def get_by_name(self, name: str) -> Language:
        return self._session.exec(select(Language).where(Language.name == name)).one()

    