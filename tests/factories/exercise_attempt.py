from typing import Optional, Protocol

import pytest
from sqlmodel import Session

from app.models.attempt import Attempt
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink
from app.models.user import User
from tests.factories.exercise import ExerciseFactory
from tests.factories.user import UserFactory


DEFAULT_SCORE = 0

class ExerciseAttemptFactory(Protocol):
    def __call__(self, user: Optional[User] = None, exercise: Optional[Exercise] = None, score: int = DEFAULT_SCORE) -> ExerciseAttempt:
        ...

@pytest.fixture
def make_exercise_attempt(session: Session, make_exercise: ExerciseFactory, make_user: UserFactory) -> ExerciseAttemptFactory:
    def make(user: Optional[User] = None, exercise: Optional[Exercise] = None, score: int = DEFAULT_SCORE) -> ExerciseAttempt:
        if user is None:
            user = make_user()
        if exercise is None:
            exercise = make_exercise()

        attempt = Attempt(user_id=user.id, score=score)
        session.add(attempt)
        session.commit()
        session.refresh(attempt)

        exercise_attempt = ExerciseAttempt(id=attempt.id, exercise_id=exercise.id)
        session.add(exercise_attempt)
        session.commit()
        session.refresh(exercise_attempt)

        phoneme_links = [
        ExerciseAttemptPhonemeLink(
            exercise_attempt_id=exercise_attempt.id,
            expected_phoneme_id=p.id,
            actual_phoneme_id=p.id,
            index=i
        )
        for i, p in enumerate(exercise.word.phonemes)
        ]
        session.add_all(phoneme_links)
        session.commit()

        return exercise_attempt
    return make
