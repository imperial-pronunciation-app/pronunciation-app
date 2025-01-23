from fastapi.testclient import TestClient

from app.routers.recording import dispatch_to_model


def test_model_dispatch(client: TestClient) -> None:
    """Test that dispatch_to_model returns corresponding text for a given audio

    Args:
        client (TestClient): TestClient for FastAPI
    """

    # Using "with" to run lifespan function in test
    with client as _:
        assert dispatch_to_model("tests/assets/hardware.wav") == "hardware"
        assert dispatch_to_model("tests/assets/software.wav") == "software"
