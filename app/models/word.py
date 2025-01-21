from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, SQLModel


if TYPE_CHECKING:
    pass



# Possible words the user can pronounce
class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str
