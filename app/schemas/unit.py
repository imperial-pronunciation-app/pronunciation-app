from typing import List, Optional

from pydantic import BaseModel

from app.models.base.unit_base import UnitBase
from app.schemas.lesson import LessonResponse


class UnitPublicWithLessons(UnitBase):
    lessons: List[LessonResponse]
    recap_lesson: Optional[LessonResponse]


class UnitsResponse(BaseModel):
    units: List[UnitPublicWithLessons]
