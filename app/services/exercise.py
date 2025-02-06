from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.user import User


class ExerciseService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def is_completed_by(self, exercise: Exercise, user: User) -> bool:
        """Returns True if the user has completed this exercise. i.e. if exercise was attempted"""
        return self._uow.attempts.find_by_user_id_and_exercise_id(user.id, exercise.id) != []