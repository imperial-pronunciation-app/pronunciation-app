# import pytest
# from sqlmodel import Session

# from app.crud.leaderboard_user_repository import LeaderboardUserRepository
# from app.models.leaderboard_user import League


# @pytest.fixture(name="repository")
# def leaderboard_repo(session: Session) -> LeaderboardUserRepository:
#     return LeaderboardUserRepository(session)


# def test_update_xp_no_record(repository: LeaderboardUserRepository) -> None:
#     # Pre
#     user_id = 1
#     league = League.GOLD
#     xp_gain = 100

#     # When
#     result = repository.update_xp(user_id, league, xp_gain)

#     # Then
#     assert result.user_id == user_id
#     assert result.league == league
#     assert result.xp == xp_gain

#     # When
#     result2 = repository.get_user_entry(user_id)

#     # Then
#     assert result2
#     assert result2.user_id == user_id
#     assert result2.league == league
#     assert result2.xp == xp_gain


# def test_update_xp_existing_record(repository: LeaderboardUserRepository) -> None:
#     # Pre
#     user_id = 1
#     league = League.GOLD
#     xp_gain = 100

#     # When
#     result = repository.update_xp(user_id, league, xp_gain)

#     # Then
#     assert result.user_id == user_id
#     assert result.league == league
#     assert result.xp == xp_gain

#     # Pre
#     xp_gain = 50

#     # When
#     result2 = repository.update_xp(user_id, league, xp_gain)

#     # Then
#     assert result2.user_id == user_id
#     assert result2.league == league
#     assert result2.xp == 150

#     # When
#     result3 = repository.get_user_entry(user_id)

#     # Then
#     assert result3
#     assert result3.user_id == user_id
#     assert result3.league == league
#     assert result3.xp == 150


# def test_get_current_leaderboard(repository: LeaderboardUserRepository) -> None:
#     # Pre
#     league = League.GOLD
#     user_ids = [i for i in range(6)]
#     xp_gains = [100, 50, 200, 75, 150, 25]
#     for user_id, xp_gain in zip(user_ids, xp_gains):
#         repository.update_xp(user_id, league, xp_gain)
    
#     # When
#     result = repository.get_global_leaderboard(league)

#     # Then
#     assert len(result) == 5
#     assert result[0].xp == 200
#     assert result[1].xp == 150
#     assert result[2].xp == 100
#     assert result[3].xp == 75
#     assert result[4].xp == 50


# def test_reset_leaderboard(repository: LeaderboardUserRepository) -> None:
#     # Pre
#     league = League.GOLD
#     user_ids = [i for i in range(3)]
#     xp_gains = [100, 50, 200]
#     for user_id, xp_gain in zip(user_ids, xp_gains):
#         repository.update_xp(user_id, league, xp_gain)
    
#     # When
#     repository.reset_leaderboard()

#     # Then
#     result = repository.get_global_leaderboard(league)
#     assert not result
#     for user_id in user_ids:
#         entry = repository.get_user_entry(user_id)
#         assert not entry
