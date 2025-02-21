from sqladmin import ModelView

from app.models import WordOfDay


class WordOfDayAdmin(ModelView, model=WordOfDay): # type: ignore[call-arg]
    column_list = [WordOfDay.id, WordOfDay.word_id, WordOfDay.date, WordOfDay.created_at, WordOfDay.word]
    column_searchable_list = [WordOfDay.date]
    column_sortable_list = [WordOfDay.id, WordOfDay.word_id, WordOfDay.date, WordOfDay.created_at]
