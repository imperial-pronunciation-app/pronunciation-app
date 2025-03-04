from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.id_model import IdModel
from app.models.unit import Unit


if TYPE_CHECKING:
    from app.models.word import Word


class Language(IdModel, table=True):
    name: str
    words: List["Word"] = Relationship(back_populates="language")
    units: List["Unit"] = Relationship(back_populates="language")