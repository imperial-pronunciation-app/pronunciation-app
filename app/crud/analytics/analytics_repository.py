from typing import Any, Sequence, Tuple

from sqlmodel import Session, col, func, select

from app.database import engine
from app.models.analytics.analytics import EndpointAnalytics
from app.models.attempt import Attempt
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink
from app.models.phoneme import Phoneme
from app.models.word import Word


class AnalyticsRepository:
    def get_count_of_endpoint_and_response_time(self) -> Sequence[Tuple[str, int, Any]]:
        with Session(engine) as session:
            stmt = select(
                EndpointAnalytics.endpoint,
                func.count(col(EndpointAnalytics.endpoint)).label("count"),
                func.avg(EndpointAnalytics.duration).label("avg_response_time"),
            ).group_by(EndpointAnalytics.endpoint)

            results: Sequence[Tuple[str, int, Any]] = session.exec(stmt).fetchall()
            return results

    def upsert_analytics(self, analytics: EndpointAnalytics) -> None:
        with Session(engine) as session:
            session.add(analytics)
            session.commit()

    def get_exercise_analytics(self) -> Sequence[Tuple[str, int]]:
        with Session(engine) as session:
            stmt = (
                select(
                    EndpointAnalytics.endpoint,
                    func.count(col(EndpointAnalytics.endpoint)).label("count"),
                )
                .where(col(EndpointAnalytics.endpoint).contains("exercise"))
                .where(~col(EndpointAnalytics.endpoint).contains("admin"))
                .group_by(EndpointAnalytics.endpoint)
                .order_by("count")  # type: ignore[arg-type]
            )

            result = session.exec(stmt).fetchall()
            return result

    def get_exercise_difficulty_analytics(self) -> Sequence[Tuple[int, float]]:
        with Session(engine) as session:
            stmt = (
                select(
                    Exercise.id,
                    func.avg(Attempt.score).label("average_score"),
                )
                .join(ExerciseAttempt, col(ExerciseAttempt.exercise_id) == col(Exercise.id))
                .join(Attempt, col(Attempt.id) == col(ExerciseAttempt.id))
                .group_by(col(Exercise.id))
                .order_by("average_score")  # Order by difficulty (lower scores first)
            )

            return session.exec(stmt).fetchall()

    def get_exercise_words(self) -> Sequence[Tuple[int, str]]:
        with Session(engine) as session:
            stmt = select(
                Exercise.id,
                Word.text,
            ).join(Word, col(Word.id) == col(Exercise.word_id))

            return session.exec(stmt).fetchall()

    def get_phoneme_difficulty_analytics(self) -> Sequence[Tuple[int | None, int | None]]:
        with Session(engine) as session:
            stmt = select(
                col(ExerciseAttemptPhonemeLink.expected_phoneme_id),
                col(ExerciseAttemptPhonemeLink.actual_phoneme_id),
            )

            return session.exec(stmt).fetchall()

    def get_phoneme_names(self) -> Sequence[Tuple[int, str, str]]:
        with Session(engine) as session:
            stmt = select(Phoneme.id, Phoneme.ipa, Phoneme.respelling).distinct()

            return session.exec(stmt).fetchall()
