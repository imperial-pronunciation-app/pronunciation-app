from typing import Optional, Protocol

import pytest
from sqlmodel import Session

from app.models.language import Language
from app.models.word_of_day import WordOfDay
from tests.factories.language import LanguageFactory
from tests.factories.word import DEFAULT_TEXT, WordFactory


class WordOfDayFactory(Protocol):
    def __call__(self, text: str = DEFAULT_TEXT, language: Optional[Language] = None) -> WordOfDay:
        ...

@pytest.fixture
def make_word_of_day(session: Session, make_word: WordFactory, make_language: LanguageFactory) -> WordOfDayFactory:
    def make(text: str = DEFAULT_TEXT, language: Optional[Language] = None) -> WordOfDay:
        if language is None:
            language = make_language()
        word = make_word(text=text, language=language)
        word_of_day = WordOfDay(word_id=word.id)
        session.add(word_of_day)
        session.commit()
        session.refresh(word_of_day)
        return word_of_day
    return make