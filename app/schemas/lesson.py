from typing import Optional

from pydantic import BaseModel


class LessonResponse(BaseModel):
    id: int
    title: str
    first_exercise_id: int
    is_completed: bool
    is_locked: bool
    stars: Optional[int]