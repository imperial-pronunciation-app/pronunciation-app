from app.crud.unit_of_work import UnitOfWork


class WordOfDayService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def change_word_of_day(self) -> None:
        word = self._uow.words.get_word_not_used_for(days=365)
        self._uow.word_of_day.add_word_of_day(word_id=word.id)
