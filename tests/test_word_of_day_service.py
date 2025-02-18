from app.crud.unit_of_work import UnitOfWork
from app.models.word import Word
from app.services.word_of_day import WordOfDayService


def test_assign_new_word_of_day(uow: UnitOfWork, sample_word: Word) -> None:
    """Tests the adding of a new word of the day to the database."""

    # When
    WordOfDayService(uow).change_word_of_day()

    # Then
    word_of_day = uow.word_of_day.get_word_of_day()
    assert word_of_day.id is sample_word.id
    assert word_of_day.word_id is sample_word.id
