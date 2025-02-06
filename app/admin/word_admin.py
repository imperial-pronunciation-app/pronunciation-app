from sqladmin import ModelView

from app.models import Word


class WordAdmin(ModelView, model=Word): # type: ignore[call-arg]
    column_list = [Word.id, Word.word]
    column_searchable_list = [Word.word]
    column_sortable_list = [Word.id, Word.word]
