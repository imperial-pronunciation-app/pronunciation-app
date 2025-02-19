# import pytest
from pytest_mock import mocker

from app.services.attempts import AttemptService


def test_word_of_day_attempts() -> None:
    """Test post_word_of_day_attempt"""

    # BASIC TEST SKELETON
    mock_service = mocker.Mock(spec=AttemptService)
    mocker.patch("app.routers.attempts.AttemptService", return_value=mock_service)

    # When

    # Then
    pass
