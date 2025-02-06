from typing import Optional

from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.user import User


class ExerciseService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def previous_exercise(self, exercise: Exercise) -> Optional[Exercise]:
        """Returns the previous exercise within the lesson, or None if it's the first exercise."""
        return exercise.lesson.exercises[exercise.index - 1] if exercise.index > 0 else None

    def next_exercise(self, exercise: Exercise) -> Optional[Exercise]:
        """Returns the next exercise within the lesson, or None if it's the last exercise."""
        return exercise.lesson.exercises[exercise.index + 1] if exercise.index < len(exercise.lesson.exercises) - 1 else None


    def is_completed_by(self, exercise: Exercise, user: User) -> bool:
        """Returns True if the user has completed this exercise. i.e. if exercise was attempted"""
        return self._uow.attempts.find_by_user_id_and_exercise_id(user.id, exercise.id) != []