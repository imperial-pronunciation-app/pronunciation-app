from typing import Awaitable, List

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.unit import Unit
from app.models.word import Word
from app.models.word_phoneme_link import WordPhonemeLink


@pytest.fixture
async def sample_units(sample_exercise: Awaitable[Exercise]) -> List[Unit]:
    return [(await sample_exercise).lesson.unit]

@pytest.fixture
async def sample_unit(session: AsyncSession) -> Unit:
    """Fixture to create a unit for lessons."""
    unit = Unit(name="Test Unit", description="Test Description", order=0)
    session.add(unit)
    await session.commit()
    await session.refresh(unit)
    return unit

@pytest.fixture
async def sample_lesson(session: AsyncSession, sample_unit: Unit) -> Lesson:
    """Fixture to create a lesson for exercises."""
    lesson = Lesson(title="Test Lesson", unit_id=sample_unit.id, order=0)
    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)
    return lesson


@pytest.fixture
async def sample_words(session: AsyncSession) -> List[Word]:
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
    await session.commit()

    for word in words:
        await session.refresh(word)

    for phoneme in phonemes:
        await session.refresh(phoneme)

    word_phoneme_links = [
        WordPhonemeLink(word_id=pat.id, phoneme_id=phonemes[0].id, index=0),
        WordPhonemeLink(word_id=pat.id, phoneme_id=phonemes[1].id, index=1),
        WordPhonemeLink(word_id=pat.id, phoneme_id=phonemes[2].id, index=2),
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[2].id, index=0),
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[1].id, index=1),
        WordPhonemeLink(word_id=tap.id, phoneme_id=phonemes[0].id, index=2)
    ]

    session.add_all(word_phoneme_links)
    await session.commit()

    for word in words:
        await session.refresh(word)

    return words

@pytest.fixture
async def sample_exercises(session: AsyncSession, sample_lesson: Lesson, sample_words: List[Word]) -> List[Exercise]:
    """Fixture to create 3 exercises with words containing phonemes."""
    exercises = [
        Exercise(lesson_id=sample_lesson.id, word_id=sample_words[0].id, index=0),
        Exercise(lesson_id=sample_lesson.id, word_id=sample_words[1].id, index=1),
        Exercise(lesson_id=sample_lesson.id, word_id=sample_words[0].id, index=2)
    ]
    session.add_all(exercises)
    await session.commit()

    for exercise in exercises:
        await session.refresh(exercise)

    return exercises

@pytest.fixture
async def sample_exercise(sample_exercises: Awaitable[List[Exercise]]) -> Exercise:
    """Fixture to return a single exercise."""
    return (await sample_exercises)[1]
