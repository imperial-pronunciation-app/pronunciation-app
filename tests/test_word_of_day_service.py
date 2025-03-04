from datetime import date

from app.crud.unit_of_work import UnitOfWork
from app.services.word_of_day import WordOfDayService
from tests.factories.word import WordFactory


def test_assign_new_word_of_day(uow: UnitOfWork, make_word: WordFactory) -> None:
    """Tests the adding of a new word of the day to the database."""
    word = make_word()

    # When
    WordOfDayService(uow).change_word_of_day()

    # Then
    word_of_day = uow.word_of_day.get_word_of_day(word.language.id)
    assert word_of_day.id is word.id
    assert word_of_day.word_id is word.id


def test_word_of_day_assigned_as_such(uow: UnitOfWork, make_word: WordFactory) -> None:
    """Tests that the word of the day is assigned the correct date"""
    word = make_word()

    # When
    WordOfDayService(uow).change_word_of_day()

    # Then
    word_of_day = uow.word_of_day.get_word_of_day(word.language.id)
    assert word_of_day.date == date.today()
    assert word_of_day.word_id == word.id
