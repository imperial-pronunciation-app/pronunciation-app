from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base.unit_base import UnitBase
from app.models.user import User
from app.schemas.unit import UnitPublicWithLessons


if TYPE_CHECKING:
    from app.models.lesson import Lesson


class Unit(UnitBase, table=True):
    order: int
    lessons: List["Lesson"] = Relationship(back_populates="unit", cascade_delete=True)

    def to_public_with_lessons(self, user: User) -> "UnitPublicWithLessons":
        return UnitPublicWithLessons(
            id=self.id,
            name=self.name,
            description=self.description,
            lessons=[lesson.to_response(user) for lesson in self.lessons]
        )