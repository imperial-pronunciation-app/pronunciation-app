import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.routers.recording import create_wav_file
from app.schemas.recording import RecordingRequest
from app.utils.similarity import similarity


def test_create_wav_file(mocker: MockerFixture) -> None:
    recording_request = RecordingRequest(audio_bytes=b"test")
    
    mock_file = mocker.mock_open()
    mocker.patch("builtins.open", mock_file)
    
    filename = create_wav_file(recording_request)
    
    mock_file.assert_called_once_with(filename, "bx")
    mock_file().write.assert_called_once_with(recording_request.audio_bytes)

@pytest.mark.parametrize("s1, s2, expected", [
    ("abc", "abc", 100),
    ("abc", "def", 0),
    ("abc", "abd", 67),
    ("abc", "abcd", 75),
    ("abc", "acbd", 50),
    ("abc", "cab", 33)])
def test_similarity(s1: str, s2: str, expected: int) -> None:
    assert similarity(s1, s2) == expected
    

def test_recording_feedback(seeded_client: TestClient, mocker: MockerFixture) -> None:
    word = seeded_client.get("/api/v1/random_word").json()

    wav_file_path = f"tests/assets/{word['word']}.wav"
    mocker.patch("app.routers.recording.upload_wav_to_s3", return_value="1.wav")
    
    with seeded_client as _, open(wav_file_path, "rb") as f:
        files = {
            "audio_file": f
        }
        recording_response = seeded_client.post(f"/api/v1/words/{word['word_id']}/recording", files=files)
        assert recording_response.status_code == 200
        assert recording_response.json() == {
            "recording_id": 1,
            "score": 100,
            "recording_phonemes": [],
        }
