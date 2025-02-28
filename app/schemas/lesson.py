from typing import List, Optional

from pydantic import BaseModel


class ListedLessonResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    is_locked: bool
    stars: Optional[int]

class LessonResponse(BaseModel):
    id: int
    title: str
    exercise_ids: List[int]
    current_exercise_index: int
