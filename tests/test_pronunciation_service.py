from typing import List, Optional, Tuple

import pytest

from app.crud.unit_of_work import UnitOfWork
from app.schemas.phoneme import PhonemePublic
from app.services.pronunciation import PronunciationService
from tests.factories.phoneme import PhonemeFactory
from tests.factories.word import WordFactory


@pytest.mark.parametrize(
    "pronounced_phonemes, expected_alignment, min_score, max_score",
    [
        # Perfect match (100%)
        (["t", "e", "s", "t"],
         [("t", "t"), ("e", "e"), ("s", "s"), ("t", "t")], 100, 100),
        
        # Substituted phoneme (small penalty)
        (["t", "ɛ", "s", "t"],  # "e" → "ɛ"
         [("t", "t"), ("e", "ɛ"), ("s", "s"), ("t", "t")], 70, 100),

        # Extra garbage phoneme (small penalty)
        (["t", "e", "s", "t", "x"],  # Extra "x"
         [("t", "t"), ("e", "e"), ("s", "s"), ("t", "t"), (None, "x")], 70, 100),

        # Missing phoneme (medium penalty)
        (["t", "s", "t"],  # Missing "e"
         [("t", "t"), ("e", None), ("s", "s"), ("t", "t")], 50, 100),

        # Completely incorrect pronunciation (high penalty)
        (["p", "a", "k", "s"],  # Wrong phonemes
         [("t", "p"), ("e", "a"), ("s", "k"), ("t", "s")], 0, 50),

        # Empty user input (0% score)
        ([],  
         [("t", None), ("e", None), ("s", None), ("t", None)], 0, 0),

        # Single phoneme
        (["t"],
         [("t", None), ("e", None), ("s", None), ("t", "t")], 0, 100),
    ]
)
def test_match_pronunciation(make_word: WordFactory, make_phoneme: PhonemeFactory, pronounced_phonemes: List[str], expected_alignment: List[Tuple[Optional[PhonemePublic], Optional[PhonemePublic]]], min_score: int, max_score: int, uow: UnitOfWork) -> None:
    """Tests phoneme alignment and pronunciation scoring across various cases."""
    word = make_word(text="test")

    # Ensure all pronounced phonemes are in the database
    for phoneme in pronounced_phonemes:
        if phoneme not in [p.ipa for p in word.phonemes]:
            make_phoneme(ipa=phoneme, language=word.language)

    alignment, score = PronunciationService(uow).evaluate_pronunciation(word, pronounced_phonemes)

    assert min_score <= score <= max_score, f"Score {score} out of range ({min_score}-{max_score})"
    alignment_ipa = [(exp.ipa if exp else None, act.ipa if act else None) for exp, act in alignment]
    assert alignment_ipa == expected_alignment, f"Unexpected alignment: {alignment}"