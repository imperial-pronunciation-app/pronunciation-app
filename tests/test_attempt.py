# test the attempt service and router

"""Service tests
"""

import os

import dotenv
import responses

from app.crud.unit_of_work import UnitOfWork
from app.routers.attempts import AttemptService


dotenv.load_dotenv()


@responses.activate
def test_successful_request(uow: UnitOfWork) -> None:
    """Test that a successful request returns a 200 status code

    Args:
        client (TestClient): TestClient for FastAPI
    """

    test_word_phonemes = ["s", "oʊ", "f", "t", "w", "ɛ", "r"]
    test_wav_filename = "tests/assets/software.wav"

    rsp = responses.Response(
        method="POST",
        url=f"{os.environ.get('MODEL_API_URL', '')}/api/v1/eng/infer_phonemes",
        json={"success": True, "phonemes": test_word_phonemes},
    )
    responses.add(rsp)

    model_response = AttemptService(uow).dispatch_to_model(test_wav_filename)
    assert model_response.phonemes == test_word_phonemes

@responses.activate
def test_unsuccessful_request(uow: UnitOfWork) -> None:
    """Test that a request with unsuccesfull inference
    raises a 200 with no b ody

    Args:
        client (TestClient): TestClient for FastAPI
    """

    test_wav_filename = "tests/assets/software.wav"

    rsp = responses.Response(
        method="POST",
        url=f"{os.environ.get('MODEL_API_URL', '')}/api/v1/eng/infer_phonemes",
        json={"success": False, "phonemes": []},
    )
    responses.add(rsp)

    model_response = AttemptService(uow).dispatch_to_model(test_wav_filename)
    assert not model_response.success

