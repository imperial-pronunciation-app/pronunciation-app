from sqladmin import ModelView

from app.models import LeaderboardUser


class LeaderboardUserAdmin(ModelView, model=LeaderboardUser): # type: ignore[call-arg]
    column_list = [LeaderboardUser.id, LeaderboardUser.user_id, LeaderboardUser.league, LeaderboardUser.xp, LeaderboardUser.created_at, LeaderboardUser.updated_at]
    column_searchable_list = [LeaderboardUser.league]
    column_sortable_list = [LeaderboardUser.id, LeaderboardUser.user_id, LeaderboardUser.league, LeaderboardUser.xp, LeaderboardUser.created_at, LeaderboardUser.updated_at]
