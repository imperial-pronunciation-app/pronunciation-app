from typing import List

import pytest
from sqlmodel import Session

from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.unit import Unit
from app.models.word import Word
from app.models.word_phoneme_link import WordPhonemeLink


@pytest.fixture
def sample_units(sample_exercise: Exercise) -> List[Unit]:
    return [sample_exercise.lesson.unit]

@pytest.fixture
def sample_unit(session: Session) -> Unit:
    """Fixture to create a unit for lessons."""
    unit = Unit(name="Test Unit", description="Test Description", order=0)
    session.add(unit)
    session.commit()
    session.refresh(unit)
    return unit

@pytest.fixture
def sample_lesson(session: Session, sample_unit: Unit) -> Lesson:
    """Fixture to create a lesson for exercises."""
    lesson = Lesson(title="Test Lesson", unit_id=sample_unit.id, order=0)
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson


@pytest.fixture
def sample_words(session: Session) -> List[Word]:
    """Fixture to create sample words and phonemes, linking them properly."""
    pat = Word(text="pat")
    tap = Word(text="tap")
    words = [pat, tap]

    phonemes = [
        Phoneme(ipa="p", respelling="p"),
        Phoneme(ipa="a", respelling="a"),
        Phoneme(ipa="t", respelling="t")
    ]

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
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[0].id, index=2)
    ]

    session.add_all(word_phoneme_links)
    session.commit()

    for word in words:
        session.refresh(word)

    return words

@pytest.fixture
def sample_exercises(session: Session, sample_lesson: Lesson, sample_words: List[Word]) -> List[Exercise]:
    """Fixture to create 3 exercises with words containing phonemes."""
    exercises = [
        Exercise(lesson_id=sample_lesson.id, word_id=sample_words[0].id, index=0),
        Exercise(lesson_id=sample_lesson.id, word_id=sample_words[1].id, index=1),
        Exercise(lesson_id=sample_lesson.id, word_id=sample_words[0].id, index=2)
    ]
    session.add_all(exercises)
    session.commit()

    for exercise in exercises:
        session.refresh(exercise)

    return exercises

@pytest.fixture
def sample_exercise(sample_exercises: List[Exercise]) -> Exercise:
    """Fixture to return a single exercise."""
    return sample_exercises[1]

@pytest.fixture
def sample_first_exercise(sample_exercises: List[Exercise]) -> Exercise:
    """Fixture to return a single exercise."""
    return sample_exercises[0]

@pytest.fixture
def sample_last_exercise(sample_exercises: List[Exercise]) -> Exercise:
    """Fixture to return a single exercise."""
    return sample_exercises[2]