from sqlmodel import Field

from app.models.id_model import IdModel


class RecapLesson(IdModel, table=True):
    id: int = Field(primary_key=True, foreign_key="lesson.id")
    user_id: int = Field(foreign_key="user.id")
    unit_id: int = Field(foreign_key="unit.id")