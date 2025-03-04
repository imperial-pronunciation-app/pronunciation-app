
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.phoneme import Phoneme


class PhonemeRespelling(SQLModel, table=True):
    phoneme_id: int = Field(foreign_key="phoneme.id", primary_key=True)
    phoneme: "Phoneme" = Relationship(back_populates="respellings")
    language_id: int = Field(foreign_key="language.id", primary_key=True)
    respelling: str