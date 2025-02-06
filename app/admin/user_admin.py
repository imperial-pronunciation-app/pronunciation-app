from sqladmin import ModelView

from app.models.user import User


class UserAdmin(ModelView, model=User): # type: ignore[call-arg]
    pk_columns = [User.id]
    column_list = [User.id, User.email, User.is_active, User.is_superuser, User.is_verified]
    column_searchable_list = [User.email]
    column_sortable_list = [User.id, User.email, User.is_active, User.is_superuser, User.is_verified]
