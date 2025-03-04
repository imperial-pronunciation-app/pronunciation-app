from typing import Optional, Protocol

import pytest
from sqlmodel import Session

from app.models.language import Language
from app.models.unit import Unit
from tests.factories.language import LanguageFactory


DEFAULT_INDEX = 0
DEFAULT_NAME = "Test Unit"
DEFAULT_DESCRIPTION = "Test Description"

class UnitFactory(Protocol):
    def __call__(self, language: Optional[Language] = None, name: str = DEFAULT_NAME, description: str = DEFAULT_DESCRIPTION, index: int = DEFAULT_INDEX) -> Unit:
        ...

@pytest.fixture
def make_unit(session: Session, make_language: LanguageFactory) -> UnitFactory:
    def make(language: Optional[Language] = None, name: str = DEFAULT_NAME, description: str = DEFAULT_DESCRIPTION, index: int = DEFAULT_INDEX) -> Unit:
        if language is None:
            language = make_language()
        unit = Unit(name=name, description=description, language_id=language.id, index=index)
        session.add(unit)
        session.commit()
        session.refresh(unit)
        return unit
    return make
