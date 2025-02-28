from typing import List, Optional

from pydantic import BaseModel

from app.models.base.unit_base import UnitBase
from app.schemas.lesson import ListedLessonResponse


class UnitPublicWithLessons(UnitBase):
    lessons: Optional[List[ListedLessonResponse]]
    recap_lesson: Optional[ListedLessonResponse]
    is_completed: bool
    is_locked: bool


class UnitsResponse(BaseModel):
    units: List[UnitPublicWithLessons]
