
from app.models.id_model import IdModel


# Possible words the user can pronounce
class Word(IdModel, table=True):
    word: str
