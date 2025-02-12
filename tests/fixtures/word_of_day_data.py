
import pytest
from sqlmodel import Session

from app.models.phoneme import Phoneme
from app.models.word import Word
from app.models.word_of_day import WordOfDay
from app.models.word_phoneme_link import WordPhonemeLink


@pytest.fixture
def sample_word_of_day(session: Session) -> WordOfDay:
    """Fixture to return a sample word of day."""
    pat = Word(text="pat")
    tap = Word(text="tap")
    words = [pat, tap]

    phonemes = [Phoneme(ipa="p", respelling="p"), Phoneme(ipa="a", respelling="a"), Phoneme(ipa="t", respelling="t")]

    session.add_all(words)
    session.add_all(phonemes)
    session.commit()

    for word in words:
        session.refresh(word)

    for phoneme in phonemes:
        session.refresh(phoneme)

    word_phoneme_links = [
        WordPhonemeLink(word_id=pat.id, phoneme_id=phonemes[0].id, index=0),
        WordPhonemeLink(word_id=pat.id, phoneme_id=phonemes[1].id, index=1),
        WordPhonemeLink(word_id=pat.id, phoneme_id=phonemes[2].id, index=2),
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[2].id, index=0),
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[1].id, index=1),
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[0].id, index=2),
    ]

    session.add_all(word_phoneme_links)
    session.commit()

    for word in words:
        session.refresh(word)

    word_of_day = WordOfDay(word_id=1)
    session.add(word_of_day)
    session.commit()
    session.refresh(word_of_day)

    return word_of_day