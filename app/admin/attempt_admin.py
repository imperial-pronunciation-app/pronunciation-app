from sqladmin import ModelView

from app.models import Attempt


class AttemptAdmin(ModelView, model=Attempt): # type: ignore[call-arg]
    column_list = [Attempt.id, Attempt.exercise_id, Attempt.user_id, Attempt.created_at, Attempt.exercise]
    column_sortable_list = [Attempt.id, Attempt.exercise_id, Attempt.user_id, Attempt.created_at]
