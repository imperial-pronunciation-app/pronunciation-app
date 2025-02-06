from sqladmin import ModelView

from app.models import Phoneme


class PhonemeAdmin(ModelView, model=Phoneme): # type: ignore[call-arg]
    column_list = [Phoneme.id, Phoneme.ipa, Phoneme.respelling, Phoneme.words]
    column_searchable_list = [Phoneme.ipa, Phoneme.respelling]
    column_sortable_list = [Phoneme.id, Phoneme.ipa, Phoneme.respelling]
