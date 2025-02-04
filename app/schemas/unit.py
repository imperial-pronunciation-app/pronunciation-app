from typing import List

from pydantic import BaseModel

from app.models.base.unit_base import UnitBase
from app.schemas.lesson import LessonResponse


class UnitPublicWithLessons(UnitBase):
    lessons: List[LessonResponse]


class UnitsResponse(BaseModel):
    units: List[UnitPublicWithLessons]
