from sqladmin import ModelView

from app.models import User


class UserAdmin(ModelView, model=User): # type: ignore[call-arg]
    column_list = [User.id, User.email, User.login_streak, User.last_login_date, User.xp_total, User.level, User.new_user, User.leaderboard_entry, User.is_active, User.is_superuser, User.is_verified]
    column_searchable_list = [User.email]
    column_sortable_list = [User.id, User.email, User.login_streak, User.last_login_date, User.xp_total, User.level, User.new_user, User.is_active, User.is_superuser, User.is_verified]
