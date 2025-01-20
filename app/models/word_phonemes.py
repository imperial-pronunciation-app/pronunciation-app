from sqlmodel import Field, SQLModel


class WordPhonemes(SQLModel, table=True):
    word_id: int = Field(foreign_key="word.id", primary_key=True)
    phoneme_id: int = Field(foreign_key="phoneme.id", primary_key=True)
    index: int

    # word: Optional["Word"] = Relationship(back_populates="phonemes")
    # phoneme: Optional["Phoneme"] = Relationship(back_populates="words")
