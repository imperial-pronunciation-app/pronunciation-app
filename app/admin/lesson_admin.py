from sqladmin import ModelView

from app.models import Lesson


class LessonAdmin(ModelView, model=Lesson): # type: ignore[call-arg]
    column_list = [Lesson.id, Lesson.unit_id, Lesson.title, Lesson.order, Lesson.unit, Lesson.exercises]
    column_searchable_list = [Lesson.title]
    column_sortable_list = [Lesson.id, Lesson.unit_id, Lesson.title, Lesson.order]
