import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture
from sqlmodel import Session, select

from app.models.recording import Recording
from app.models.word import Word
from app.routers.recording import create_wav_file
from app.schemas.recording import RecordingRequest
from app.seed_data import SeedData
from app.utils.similarity import similarity


def test_create_wav_file(mocker: MockerFixture) -> None:
    recording_request = RecordingRequest(audio_bytes=b"test")

    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)

    filename = create_wav_file(recording_request)

    mock_file.assert_called_once_with(filename, "bx")
    mock_file().write.assert_called_once_with(recording_request.audio_bytes)


@pytest.mark.parametrize(
    "s1, s2, expected",
    [
        ("abc", "abc", 100),
        ("abc", "def", 0),
        ("abc", "abd", 67),
        ("abc", "abcd", 75),
        ("abc", "acbd", 50),
        ("abc", "cab", 33),
    ],
)
def test_similarity(s1: str, s2: str, expected: int) -> None:
    assert similarity(s1, s2) == expected


def test_recording_feedback(seeded_session: Session, seeded_client: TestClient, mocker: MockerFixture, test_seed_data: SeedData) -> None:
    # Check that calls to:
    # create_wav_file, upload_wav_to_s3, dispatch_to_model, similarity are made correctly
    # Recording entry is added to the table
    # File is deleted correctly
    # Correct response is returned
    test_word = "software"
    blob_id = "blob_id"
    test_wav_filename = "test.wav"

    mock_create_wav_file = mocker.patch("app.routers.recording.create_wav_file", return_value=test_wav_filename)
    mock_upload_wav_to_s3 = mocker.patch("app.routers.recording.upload_wav_to_s3", return_value=blob_id)
    mock_dispatch_to_model = mocker.patch("app.routers.recording.dispatch_to_model", return_value=test_word)
    mock_os_remove = mocker.patch("os.remove")
    mock_similarity = mocker.patch("app.routers.recording.similarity", return_value=100)

    word = seeded_session.exec(select(Word).where(Word.word == test_word)).one()

    wav_file_path = f"tests/assets/{test_word}.wav"

    with open(wav_file_path, "rb") as f:
        files = {"audio_file": f}
        recording_response = seeded_client.post(f"/api/v1/words/{word.id}/recording", files=files)
    assert recording_response.status_code == 200
    data = recording_response.json()
    assert data["score"] == 100
    recording_id = data["recording_id"]
    
    recording = seeded_session.get(Recording, recording_id)
    # TODO: Test the phonemes
    assert recording is not None
    assert recording.word_id == word.id
    
    mock_create_wav_file.assert_called_once()
    mock_upload_wav_to_s3.assert_called_once_with(test_wav_filename)
    
    mock_dispatch_to_model.assert_called_once_with(test_wav_filename)
    mock_os_remove.assert_called_once_with(test_wav_filename)
    mock_similarity.assert_called_once_with(test_word, test_word)


## test CRUD separately

## test model separately
