from typing import Optional, Protocol

import pytest
from sqlmodel import Session, select

from app.models.language import Language
from app.models.phoneme import Phoneme
from app.models.word import Word
from app.models.word_phoneme_link import WordPhonemeLink
from tests.factories.language import LanguageFactory
from tests.factories.phoneme import PhonemeFactory


DEFAULT_TEXT = "pat"

class WordFactory(Protocol):
    def __call__(self, text: str = DEFAULT_TEXT, language: Optional[Language] = None) -> Word:
        ...

@pytest.fixture
def make_word(session: Session, make_language: LanguageFactory, make_phoneme: PhonemeFactory) -> WordFactory:
    def make(text: str = DEFAULT_TEXT, language: Optional[Language] = None) -> Word:
        if language is None:
            language = make_language()
        word = Word(text=text, language_id=language.id)
        session.add(word)
        session.commit()
        session.refresh(word)

        for index, letter in enumerate(word.text):
            phoneme = session.exec(select(Phoneme).where(Phoneme.ipa == letter)).first()
            if not phoneme:
                phoneme = make_phoneme(ipa=letter, language=language)

            word_phoneme_link = WordPhonemeLink(word_id=word.id, phoneme_id=phoneme.id, index=index) # type: ignore
            session.add(word_phoneme_link)

        session.commit()
        session.refresh(word)
        return word
    return make
