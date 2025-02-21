import pytest
from pytest_mock import MockerFixture

from app.crud.unit_of_work import UnitOfWork
from app.services.attempts import AttemptService
from app.utils.similarity import similarity


def test_create_wav_file(mocker: MockerFixture, uow: UnitOfWork) -> None:
    audio_bytes = b"test"

    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    filename = AttemptService(uow).create_wav_file(audio_bytes)

    mock_file.assert_called_once_with(filename, "bx")
    mock_file().write.assert_called_once_with(audio_bytes)


@pytest.mark.parametrize(
    "s1, s2, expected",
    [
        (["a", "b", "c"], ["a", "b", "c"], 100),
        (["a", "b", "c"], ["d", "e", "f"], 0),
        (["a", "b", "c"], ["a", "b", "d"], 67),
        (["a", "b", "c"], ["a", "b", "c", "d"], 75),
        (["a", "b", "c"], ["a", "c", "b", "d"], 50),
        (["a", "b", "c"], ["c", "a", "b"], 33),
    ],
)
def test_similarity(s1: list[str], s2: list[str], expected: int) -> None:
    assert similarity(s1, s2) == expected

