from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.base.language_base import LanguageBase
from app.models.unit import Unit


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.word import Word


class Language(LanguageBase, table=True):
    is_default: bool = Field(default=False)
    words: List["Word"] = Relationship(back_populates="language")
    units: List["Unit"] = Relationship(back_populates="language")
    users: List["User"] = Relationship(back_populates="language")
