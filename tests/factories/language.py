from typing import Protocol

import pytest
from sqlmodel import Session

from app.models.language import Language


DEFAULT_NAME = "eng"

class LanguageFactory(Protocol):
    def __call__(self, name: str = DEFAULT_NAME) -> Language:
        ...

@pytest.fixture
def make_language(session: Session) -> LanguageFactory:
    def make(name: str = DEFAULT_NAME) -> Language:
        language = Language(name=name)
        session.add(language)
        session.commit()
        session.refresh(language)
        return language
    return make
