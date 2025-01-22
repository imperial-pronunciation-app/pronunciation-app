from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.routers.recording import create_wav_file
from app.schemas.recording import RecordingRequest


def test_create_wav_file(mocker: MockerFixture) -> None:
  recording_request = RecordingRequest(user_id=1, audio_bytes=b"test")
  mock_file = mocker.mock_open()
  mocker.patch("builtins.open", mock_file)
  
  filename = create_wav_file(recording_request)
  
  mock_file.assert_called_once_with(filename, "bx")
  mock_file().write.assert_called_once_with(recording_request.audio_bytes)

def test_recording_feedback(client: TestClient, mocker: MockerFixture) -> None:
  wav_file = "test.wav" # noqa: F841
  
  mock_dispatch = mocker.patch("app.routers.recording.dispatch_to_model", return_value="hardware") # noqa: F841
  
  recording_response = client.get("/api/v1/words/1/recording") # noqa: F841
# def test_read_random_word_empty(client: TestClient) -> None:
#     """Test that random_word endpoint returns 404 for an empty table

#     Args:
#         session (Session): Session for unseeded database
#         client (TestClient): TestClient for FastAPI
#     """

#     response = client.get("/api/v1/random_word")

#     assert response.status_code == 404

# @pytest.mark.parametrize("test_seed_data", [
#     SeedData(words=[
#         WordData(word="software", phonemes=["s", "oʊ", "f", "t", "w", "ɛ", "r"]),
#     ]),
#     SeedData(words=[
#         WordData(word="hardware", phonemes=["h", "ɑː", "r", "d", "w", "ɛ", "r"]),
#     ])
# ], indirect=True)
# def test_read_random_word_single(seeded_client: TestClient, test_seed_data: SeedData) -> None:
#     """Test that random_word endpoint returns a single word from a seeded table

#     Args:
#         seeded_client (TestClient): _description_
#         test_seed_data (SeedData): _description_
#     """
#     response = seeded_client.get("/api/v1/random_word")
#     data = response.json()
#     assert response.status_code == 200
#     assert data["word"] == test_seed_data.words[0].word
#     # turn on once endpoint also returns phonemes
#     assert [phoneme["ipa"] for phoneme in data["word_phonemes"]] == test_seed_data.words[0].phonemes