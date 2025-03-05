from typing import Protocol

import pytest
from sqlmodel import Session

from app.models.language import Language


DEFAULT_CODE = "eng"
DEFAULT_NAME = "English"


class LanguageFactory(Protocol):
    def __call__(self, code: str = DEFAULT_CODE, name: str = DEFAULT_NAME, is_default: bool = True) -> Language:
        ...

@pytest.fixture
def make_language(session: Session) -> LanguageFactory:
    def make(code: str = DEFAULT_CODE, name: str = DEFAULT_NAME, is_default: bool = True) -> Language:
        language = Language(code=code, name=name, is_default=is_default)
        session.add(language)
        session.commit()
        session.refresh(language)
        return language
    return make
