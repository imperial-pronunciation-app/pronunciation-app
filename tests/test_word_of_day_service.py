from datetime import date

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


def test_word_of_day_assigned_as_such(uow: UnitOfWork, sample_word: Word) -> None:
    """Tests that the word of the day is assigned the correct date"""

    # When
    WordOfDayService(uow).change_word_of_day()

    # Then
    word_of_day = uow.word_of_day.get_word_of_day()
    assert word_of_day.date == date.today()
    assert word_of_day.word_id == sample_word.id
