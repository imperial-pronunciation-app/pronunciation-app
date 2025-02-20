from typing import List

from pydantic import BaseModel

from app.schemas.lesson import LessonResponse


class UnitPublicWithLessons(BaseModel):
    id: int
    name: str
    description: str
    lessons: List[LessonResponse]

class UnitsResponse(BaseModel):
    units: List[UnitPublicWithLessons]
