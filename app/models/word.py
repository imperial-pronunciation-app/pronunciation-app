from typing import TYPE_CHECKING

from app.models.base_model import BaseModel


if TYPE_CHECKING:
    pass


# Possible words the user can pronounce
class Word(BaseModel, table=True):
    word: str
