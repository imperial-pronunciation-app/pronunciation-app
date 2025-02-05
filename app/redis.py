from typing import Dict, List, Sequence

from redis import Redis

from app.models.leaderboard_user_link import LeaderboardUserLink, League


class LRedis:
    """Leaderboard redis client"""

    _redis = Redis(host="redis")

    def __init__(self) -> None:
        raise ValueError("Do not instantiate")

    @staticmethod
    def sorted(league: League, start: int, end: int, desc: bool = True) -> List[int]:
        """Indices are inclusive as expected in redis"""

        league_key = LRedis._league_key(league)
        total_count = LRedis._redis.zcard(league_key)
        start_index = max(0, start)
        end_index = min(end, total_count - 1)

        if desc:
            return list(map(int, LRedis._redis.zrevrange(league_key, start_index, end_index)))
        else:
            return list(map(int, LRedis._redis.zrange(league_key, start_index, end_index)))

    @staticmethod
    def rank(league: League, leaderboard_user_id: int) -> int:
        r = LRedis._redis.zrevrank(LRedis._league_key(league), leaderboard_user_id)
        if r is None:
            raise ValueError(f"Leaderboard user with id {leaderboard_user_id} not found in league {league}")
        return r

    @staticmethod
    def size_of(league: League) -> int:
        return LRedis._redis.zcard(LRedis._league_key(league))
    
    @staticmethod
    def create_entry(league: League, leaderboard_user_id: int, xp: int) -> None:
        LRedis._redis.zadd(LRedis._league_key(league), {str(leaderboard_user_id): xp}, nx=True)

    @staticmethod
    def create_entry_from_user(leaderboard_user: LeaderboardUserLink) -> None:
        LRedis.create_entry(leaderboard_user.league, leaderboard_user.id, leaderboard_user.xp)

    @staticmethod
    def create_entries(league: League, user_id_to_xp: Dict[int, int]) -> None:
        """Ignores mypy type checking because it thinks Dict[str, int] is not compatible with Mapping[str | bytes, bytes | float | int | str]"""
        if not user_id_to_xp:
            return
        id_str_to_xp = {str(user_id): xp for user_id, xp in user_id_to_xp.items()}
        LRedis._redis.zadd(LRedis._league_key(league), id_str_to_xp, nx=True) # type: ignore

    @staticmethod
    def create_entries_from_users(league: League, leaderboard_users: Sequence[LeaderboardUserLink]) -> None:
        LRedis.create_entries(league, {user.id: user.xp for user in leaderboard_users})

    @staticmethod
    def update_xp(league: League, leaderboard_user_id: int, xp: int) -> None:
        assert xp >= 0
        LRedis._redis.zincrby(LRedis._league_key(league), xp, str(leaderboard_user_id))

    @staticmethod
    def clear_league(league: League) -> None:
        LRedis._redis.delete(LRedis._league_key(league))
    
    @staticmethod
    def clear() -> None:
        LRedis._redis.flushall()

    @staticmethod
    def move_all_entries(from_league: League, to_league: League) -> None:
        """Should be used for testing only"""
        LRedis._redis.zunionstore(LRedis._league_key(to_league), [LRedis._league_key(from_league), LRedis._league_key(to_league)])
        LRedis.clear_league(from_league)

    @staticmethod
    def _league_key(league: League) -> str:
        return f"leaderboard:{league}"
