
from typing import Optional

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.language import Language


class LanguageRepository(GenericRepository[Language]):

    def __init__(self, session: Session):
        super().__init__(session, Language)

    def find_by_name(self, name: str) -> Optional[Language]:
        return self._session.exec(select(Language).where(Language.name == name)).first()

    def get_default(self) -> Language:
        return self._session.exec(select(Language).where(Language.is_default)).one()
