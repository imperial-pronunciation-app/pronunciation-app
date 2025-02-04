import math
from typing import List

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user import LeaderboardUser, League
from app.models.user import User
from app.redis import create_redis_entries_from_users, create_redis_entry_from_user, get_sorted_entries, redis_client
from app.schemas.leaderboard import LeaderboardEntry, LeaderboardResponse
from app.utils.days import days_until_next_sunday


class LeaderboardService:

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    def get_global_leaderboard_for_user(self, user: User, top_k: int = 3, user_position_k: int = 2) -> LeaderboardResponse:
        leaderboard_user = self._uow.leaderboard_users.get_by_user(user.id)
        days_until_end = days_until_next_sunday()
        league = leaderboard_user.league
        league_key = f"leaderboard:{league}"

        user_rank = redis_client.zrevrank(league_key, leaderboard_user.id)
        if not user_rank:
            create_redis_entry_from_user(leaderboard_user)
            user_rank = redis_client.zrevrank(league_key, leaderboard_user.id)
            assert user_rank is not None

        top_leaderboard_user_ids = get_sorted_entries(league, 0, top_k - 1)
        user_position_leaderboard_user_ids = get_sorted_entries(league, user_rank - user_position_k, user_rank + user_position_k)

        leaders = self._leaderboard_entries_from_leaderboard_user_ids(top_leaderboard_user_ids)
        user_position = self._leaderboard_entries_from_leaderboard_user_ids(user_position_leaderboard_user_ids, user_rank - user_position_k)

        return LeaderboardResponse(
            league=league,
            days_until_end=days_until_end,
            leaders=leaders,
            user_position=user_position
        )
    
    def _leaderboard_entries_from_leaderboard_user_ids(self, leaderboard_user_ids: List[int], starting_rank: int = 0) -> List[LeaderboardEntry]:
        if starting_rank < 0:
            # For example, if a league only has 1 player, the rank should start from 1 not -1
            starting_rank = 0
        return [self._leaderboard_entry_from_leaderboard_user_id_and_rank(user_id, starting_rank + i + 1) for i, user_id in enumerate(leaderboard_user_ids)]
    
    def _leaderboard_entry_from_leaderboard_user_id_and_rank(self, leaderboard_user_id: int, rank: int) -> LeaderboardEntry:
        leaderboard_user = self._uow.leaderboard_users.get_by_id(leaderboard_user_id)
        email = self._uow.users.get_by_id(leaderboard_user.user_id).email
        return LeaderboardEntry(rank, email, leaderboard_user.xp)
    
    def reset_leaderboard(self) -> None:
        self._handle_promotions_and_demotions()
        self._log_carry_forward()
        for league in League:
            self._reset_redis(league)
        self._uow.commit()
    
    def _handle_promotions_and_demotions(self) -> None:
        bronze_promotions = self._get_promotions_for_league(League.BRONZE)
        silver_demotions = self._get_demotions_for_league(League.SILVER)
        silver_promotions = self._get_promotions_for_league(League.SILVER)
        gold_demotions = self._get_demotions_for_league(League.GOLD)
        self._set_users_new_league(bronze_promotions, League.SILVER)
        self._set_users_new_league(silver_demotions, League.BRONZE)
        self._set_users_new_league(silver_promotions, League.GOLD)
        self._set_users_new_league(gold_demotions, League.SILVER)

    def _get_promotions_for_league(self, league: League) -> List[LeaderboardUser]:
        league_key = f"leaderboard:{league}"

        # Get total players in the current league
        total_count = redis_client.zcard(league_key)
        if total_count == 0:
            return []

        # Calculate top 20% indices
        top_20_cutoff = int(total_count * 0.2) - 1  # Top 20% (highest scores)

        # Get top 20% players for promotion (highest scores)
        promoted_leaderboard_user_ids = get_sorted_entries(league, 0, top_20_cutoff)
        return self._uow.leaderboard_users.get_by_ids(promoted_leaderboard_user_ids)

    def _get_demotions_for_league(self, league: League) -> List[LeaderboardUser]:
        league_key = f"leaderboard:{league}"

        # Get total players in the current league
        total_count = redis_client.zcard(league_key)
        if total_count == 0:
            return []

        # Calculate bottom 20% indices
        bottom_20_cutoff = int(total_count * 0.2) - 1  # Bottom 20% (lowest scores)

        # Get top 20% players for promotion (highest scores)
        demoted_leaderboard_user_ids = get_sorted_entries(league, 0, bottom_20_cutoff, desc=False)
        return self._uow.leaderboard_users.get_by_ids([leaderboard_user_id for leaderboard_user_id in demoted_leaderboard_user_ids])


    def _set_users_new_league(self, users: List[LeaderboardUser], new_league: League) -> None:
        for user in users:
            user.league = new_league
        self._uow.leaderboard_users.upsert_all(users)

    def _log_carry_forward(self) -> None:
        records = self._uow.leaderboard_users.all()
        for record in records:
            record.xp = int(math.log2(record.xp + 1))
        self._uow.leaderboard_users.upsert_all(records)
    
    def _reset_redis(self, league: League) -> None:
        league_key = f"leaderboard:{league}"
        redis_client.delete(league_key)
        records = self._uow.leaderboard_users.find_by_league(league)
        create_redis_entries_from_users(league, records)
