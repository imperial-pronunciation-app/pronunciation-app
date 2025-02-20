from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import Base


class WordPhonemeLink(Base):
    __tablename__ = "word_phoneme_link"

    word_id: Mapped[int] = mapped_column(ForeignKey("word.id"), primary_key=True)
    phoneme_id: Mapped[int] = mapped_column(ForeignKey("phoneme.id"), primary_key=True)
    index: Mapped[int] = mapped_column(Integer, primary_key=True)