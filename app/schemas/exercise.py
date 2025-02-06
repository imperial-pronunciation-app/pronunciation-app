from pydantic import BaseModel

from app.schemas.word import WordPublicWithPhonemes


class ExerciseResponse(BaseModel):
    id: int
    word: WordPublicWithPhonemes
    previous_exercise_id: int | None
    next_exercise_id: int | None