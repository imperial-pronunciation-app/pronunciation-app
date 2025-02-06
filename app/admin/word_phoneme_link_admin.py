from sqladmin import ModelView

from app.models import WordPhonemeLink


class WordPhonemeLinkAdmin(ModelView, model=WordPhonemeLink): # type: ignore[call-arg]
    column_list = [WordPhonemeLink.word_id, WordPhonemeLink.phoneme_id, WordPhonemeLink.index]
    column_sortable_list = [WordPhonemeLink.word_id, WordPhonemeLink.phoneme_id, WordPhonemeLink.index]
