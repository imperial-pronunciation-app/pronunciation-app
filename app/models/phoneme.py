from typing import Optional

from sqlmodel import Field, SQLModel


class Phoneme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ipa: str
    respelling: str
