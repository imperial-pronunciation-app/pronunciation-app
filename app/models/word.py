from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, SQLModel


if TYPE_CHECKING:
    pass


# Possible words the user can pronounce
class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str

    # TODO: Discuss removal - this relationship is not useful whenever we want ordered phonemes
    # (which I think is always). We have to use the link table to get the index
    # phonemes: List["Phoneme"] = Relationship(back_populates="words", link_model=WordPhonemeLink)
