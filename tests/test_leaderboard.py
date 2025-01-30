from uuid import uuid4

import pytest
from sqlmodel import Session

from app.crud.leaderboard_repository import LeaderboardRepository
from app.models.leaderboard import League


@pytest.fixture(name="repository")
def leaderboard_repo(session: Session) -> LeaderboardRepository:
    return LeaderboardRepository(session)


def test_update_xp_no_record(repository: LeaderboardRepository) -> None:
    # Pre
    user_id = uuid4()
    league = League.GOLD
    xp_gain = 100

    # When
    result = repository.update_xp(user_id, league, xp_gain)

    # Then
    assert result.user_id == user_id
    assert result.league == league
    assert result.xp == xp_gain
    assert result.current

    # When
    result2 = repository.get_user_current_entry(user_id)

    # Then
    assert result2
    assert result2.user_id == user_id
    assert result2.league == league
    assert result2.xp == xp_gain
    assert result2.current


def test_update_xp_existing_record(repository: LeaderboardRepository) -> None:
    # Pre
    user_id = uuid4()
    league = League.GOLD
    xp_gain = 100

    # When
    result = repository.update_xp(user_id, league, xp_gain)

    # Then
    assert result.user_id == user_id
    assert result.league == league
    assert result.xp == xp_gain
    assert result.current

    # Pre
    xp_gain = 50

    # When
    result2 = repository.update_xp(user_id, league, xp_gain)

    # Then
    assert result2.user_id == user_id
    assert result2.league == league
    assert result2.xp == 150
    assert result2.current

    # When
    result3 = repository.get_user_current_entry(user_id)

    # Then
    assert result3
    assert result3.user_id == user_id
    assert result3.league == league
    assert result3.xp == 150
    assert result3.current


def test_get_current_leaderboard(repository: LeaderboardRepository) -> None:
    # Pre
    league = League.GOLD
    user_ids = [uuid4() for _ in range(6)]
    xp_gains = [100, 50, 200, 75, 150, 25]
    for user_id, xp_gain in zip(user_ids, xp_gains):
        repository.update_xp(user_id, league, xp_gain)
    
    # When
    result = repository.get_current_leaderboard(league)

    # Then
    assert len(result) == 5
    assert result[0].xp == 200
    assert result[1].xp == 150
    assert result[2].xp == 100
    assert result[3].xp == 75
    assert result[4].xp == 50


def test_reset_leaderboard(repository: LeaderboardRepository) -> None:
    # Pre
    league = League.GOLD
    user_ids = [uuid4() for _ in range(3)]
    xp_gains = [100, 50, 200]
    for user_id, xp_gain in zip(user_ids, xp_gains):
        repository.update_xp(user_id, league, xp_gain)
    
    # When
    repository.reset_leaderboard()

    # Then
    result = repository.get_current_leaderboard(league)
    assert not result
    for user_id in user_ids:
        entry = repository.get_user_current_entry(user_id)
        assert not entry
