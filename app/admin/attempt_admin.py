from sqladmin import ModelView

from app.models import Attempt


class AttemptAdmin(ModelView, model=Attempt): # type: ignore[call-arg]
    column_list = [Attempt.id, Attempt.exercise_id, Attempt.user_id, Attempt.score, Attempt.created_at]
    column_sortable_list = [Attempt.id, Attempt.exercise_id, Attempt.user_id, Attempt.score, Attempt.created_at]
