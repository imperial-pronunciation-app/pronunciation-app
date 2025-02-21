from pytest_mock import MockerFixture

from app.crud.unit_of_work import UnitOfWork
from app.services.attempts import AttemptService


def test_create_wav_file(mocker: MockerFixture, uow: UnitOfWork) -> None:
    audio_bytes = b"test"

    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    filename = AttemptService(uow).create_wav_file(audio_bytes)

    mock_file.assert_called_once_with(filename, "bx")
    mock_file().write.assert_called_once_with(audio_bytes)
