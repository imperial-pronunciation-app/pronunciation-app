
from typing import Optional, Protocol

import pytest
from sqlmodel import Session

from app.models.language import Language
from app.models.phoneme import Phoneme
from app.models.phoneme_respelling import PhonemeRespelling
from tests.factories.language import LanguageFactory


DEFAULT_IPA = "p"
DEFAULT_PATH = "p.wav"

class PhonemeFactory(Protocol):
    def __call__(self, ipa: str = DEFAULT_IPA, cdn_path: str = DEFAULT_PATH, language: Optional[Language] = None) -> Phoneme:
        ...

@pytest.fixture
def make_phoneme(session: Session, make_language: LanguageFactory) -> PhonemeFactory:
    def make(ipa: str = DEFAULT_IPA, cdn_path: str = DEFAULT_PATH, language: Optional[Language] = None) -> Phoneme:
        if language is None:
            language = make_language()
        phoneme = Phoneme(ipa=ipa, language_id=language.id, cdn_path=cdn_path)
        session.add(phoneme)
        session.commit()
        session.refresh(phoneme)

        respelling = PhonemeRespelling(respelling=ipa, phoneme_id=phoneme.id, language_id=language.id)
        session.add(respelling)
        session.commit()
        
        return phoneme
    return make