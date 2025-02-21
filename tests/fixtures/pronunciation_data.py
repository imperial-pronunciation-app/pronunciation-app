from typing import List

import pytest
from sqlmodel import Session

from app.models.phoneme import Phoneme
from app.models.word import Word
from app.models.word_phoneme_link import WordPhonemeLink


@pytest.fixture
def sample_pronunciation_phonemes(session: Session) -> List[Phoneme]:
    phonemes = [
        Phoneme(ipa="t", respelling="t"),
        Phoneme(ipa="ɛ", respelling="e"),
        Phoneme(ipa="s", respelling="s"),
        Phoneme(ipa="p", respelling="p"),
        Phoneme(ipa="a", respelling="a"),
        Phoneme(ipa="k", respelling="k"),
        Phoneme(ipa="x", respelling="x"),
        Phoneme(ipa="e", respelling="e"),
        Phoneme(ipa="<unknown>", respelling="unknown"),
    ]

    session.add_all(phonemes)
    session.commit()  

    return phonemes

@pytest.fixture
def sample_pronunciation_word(session: Session, sample_pronunciation_phonemes: List[Phoneme]) -> Word:
    """Fixture to create sample words and phonemes, linking them properly."""
    test = Word(text="test")

    session.add(test)
    session.commit()

    for phoneme in sample_pronunciation_phonemes:
        session.refresh(phoneme)

    word_phoneme_links = [
        WordPhonemeLink(word_id=test.id, phoneme_id=sample_pronunciation_phonemes[0].id, index=0),
        WordPhonemeLink(word_id=test.id, phoneme_id=sample_pronunciation_phonemes[1].id, index=1),
        WordPhonemeLink(word_id=test.id, phoneme_id=sample_pronunciation_phonemes[2].id, index=2),
        WordPhonemeLink(word_id=test.id, phoneme_id=sample_pronunciation_phonemes[0].id, index=3)
    ]

    session.add_all(word_phoneme_links)
    session.commit()

    session.refresh(test)

    return test
