from typing import List, Sequence

from app.crud.unit_of_work import UnitOfWork
from app.models.language import Language
from app.schemas.language import LanguagePublic


class LanguageService:

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def to_public_sorted(self, languages: Sequence[Language]) -> List[LanguagePublic]:
        ls: List[Language] = list(languages)
        return [self._to_public(language) for language in sorted(ls, key=lambda lang: lang.name)]

    def _to_public(self, language: Language) -> LanguagePublic:
        return LanguagePublic(
            id=language.id,
            code=language.code,
            name=language.name,
        )
