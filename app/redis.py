from typing import List, Mapping, Sequence

from redis import Redis

from app.models.leaderboard_user import LeaderboardUser, League


redis_client = Redis(host="redis")


def get_sorted_entries(league: League, start: int, end: int, desc: bool = True) -> List[int]:
    """Indices are inclusive as expected in redis"""

    total_count = redis_client.zcard(f"leaderboard:{league}")
    start_index = max(0, start)
    end_index = min(end, total_count - 1)

    if desc:
        return list(map(int, redis_client.zrevrange(f"leaderboard:{league}", start_index, end_index)))
    else:
        return list(map(int, redis_client.zrange(f"leaderboard:{league}", start_index, end_index)))


def create_redis_entry(league: League, leaderboard_user_id: int, xp: int) -> None:
    redis_client.zadd(f"leaderboard:{league}", {str(leaderboard_user_id): xp}, nx=True)


def create_redis_entry_from_user(leaderboard_user: LeaderboardUser) -> None:
    create_redis_entry(leaderboard_user.league, leaderboard_user.id, leaderboard_user.xp)


def create_redis_entries(league: League, user_id_to_xp: Mapping[int, int]) -> None:
    """Ignores mypy type checking because it thinks Mapping[str, int] is not compatible with Mapping[str | bytes, bytes | float | int | str]"""
    if not user_id_to_xp:
        return
    id_str_to_xp = {str(user_id): xp for user_id, xp in user_id_to_xp.items()}
    redis_client.zadd(f"leaderboard:{league}", id_str_to_xp, nx=True) # type: ignore


def create_redis_entries_from_users(league: League, leaderboard_users: Sequence[LeaderboardUser]) -> None:
    """Ignores mypy type checking because it thinks Mapping[str, int] is not compatible with Mapping[str | bytes, bytes | float | int | str]"""
    if not leaderboard_users:
        return
    id_str_to_xp = {str(user.id): user.xp for user in leaderboard_users}
    redis_client.zadd(f"leaderboard:{league}", id_str_to_xp, nx=True) # type: ignore


def increment_redis_entry(league: League, leaderboard_user_id: int, xp: int) -> None:
    redis_client.zincrby(f"leaderboard:{league}", xp, str(leaderboard_user_id))
