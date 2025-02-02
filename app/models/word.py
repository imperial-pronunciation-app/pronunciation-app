from typing import TYPE_CHECKING

from app.models.id_model import IdModel


if TYPE_CHECKING:
    pass


# Possible words the user can pronounce
class Word(IdModel, table=True):
    word: str
