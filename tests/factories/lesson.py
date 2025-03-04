from typing import Protocol

import pytest
from sqlmodel import Session

from app.models.lesson import Lesson


DEFAULT_TITLE = "Test Lesson"

class LessonFactory(Protocol):
    def __call__(self, title: str = DEFAULT_TITLE) -> Lesson:
        ...

@pytest.fixture
def make_lesson(session: Session) -> LessonFactory:
    def make(title: str = DEFAULT_TITLE) -> Lesson:
        lesson = Lesson(title=title)
        session.add(lesson)
        session.commit()
        session.refresh(lesson)
        return lesson
    return make