from typing import List, Optional

from pydantic import BaseModel

from app.schemas.exercise import ExerciseResponse


class ListedLessonResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    is_locked: bool
    stars: Optional[int]

class LessonResponse(BaseModel):
    id: int
    title: str
    exercises: List[ExerciseResponse]
    current_exercise_index: int
