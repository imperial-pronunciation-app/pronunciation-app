from sqladmin import ModelView

from app.models import Word


class WordAdmin(ModelView, model=Word): # type: ignore[call-arg]
    column_list = [Word.id, Word.text]
    column_searchable_list = [Word.text]
    column_sortable_list = [Word.id, Word.text]
