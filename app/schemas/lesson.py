from pydantic import BaseModel


class LessonResponse(BaseModel):
    title: str
    first_exercise_id: int
    is_completed: bool