from sqladmin import ModelView

from app.models import Unit


class UnitAdmin(ModelView, model=Unit): # type: ignore[call-arg]
    column_list = [Unit.id, Unit.order, Unit.lessons]
    column_sortable_list = [Unit.id, Unit.order]
