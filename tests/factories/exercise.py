from typing import Optional, Protocol

import pytest
from sqlmodel import Session

from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.word import Word
from tests.factories.lesson import LessonFactory
from tests.factories.word import WordFactory


DEFAULT_INDEX = 0

class ExerciseFactory(Protocol):
    def __call__(self, lesson: Optional[Lesson] = None, word: Optional[Word] = None, index: int = DEFAULT_INDEX) -> Exercise:
        ...

@pytest.fixture
def make_exercise(session: Session, make_lesson: LessonFactory, make_word: WordFactory) -> ExerciseFactory:
    def make(lesson: Optional[Lesson] = None, word: Optional[Word] = None, index: int = DEFAULT_INDEX) -> Exercise:
        if lesson is None:
            lesson = make_lesson()
        if word is None:
            word = make_word()
        exercise = Exercise(lesson_id=lesson.id, word_id=word.id, index=index)
        session.add(exercise)
        session.commit()
        session.refresh(exercise)
        return exercise
    return make