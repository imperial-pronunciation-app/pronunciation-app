from typing import Optional, Protocol

import pytest
from sqlmodel import Session

from app.models.basic_lesson import BasicLesson
from app.models.unit import Unit
from tests.factories.lesson import DEFAULT_TITLE, LessonFactory
from tests.factories.unit import UnitFactory


DEFAULT_INDEX = 0

class BasicLessonFactory(Protocol):
    def __call__(self, title: str = DEFAULT_TITLE, unit: Optional[Unit] = None, index: int = DEFAULT_INDEX) -> BasicLesson:
        ...

@pytest.fixture
def make_basic_lesson(session: Session, make_lesson: LessonFactory, make_unit: UnitFactory) -> BasicLessonFactory:
    def make(title: str = DEFAULT_TITLE, unit: Optional[Unit] = None, index: int = DEFAULT_INDEX) -> BasicLesson:
        if unit is None:
            unit = make_unit()
        
        lesson = make_lesson(title=title)

        basic_lesson = BasicLesson(id=lesson.id, index=index, unit_id=unit.id)
        session.add(basic_lesson)
        session.commit()
        session.refresh(basic_lesson)
        return basic_lesson
    return make