import responses

from app.routers.recording import dispatch_to_model


@responses.activate
def test_successful_request() -> None:
    """Test that a successful request returns a 200 status code

    Args:
        client (TestClient): TestClient for FastAPI
    """

    test_word_phonemes = ['s', 'oʊ', 'f', 't', 'w', 'ɛ', 'r']
    test_wav_filename = "tests/assets/software.wav"
    
    rsp = responses.Response(
        method="POST",
        url="http://localhost:8001/api/v1/infer_phonemes",
        json={"phonemes": test_word_phonemes},
    )
    responses.add(rsp)

    assert dispatch_to_model(test_wav_filename) == test_word_phonemes
