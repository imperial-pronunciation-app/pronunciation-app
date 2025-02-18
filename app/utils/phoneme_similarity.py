from app.resources.phoneme_similarity import PHONEME_SIMILARITY


def phoneme_similarity(p1: str, p2: str) -> float:
    """Returns a similarity score between 0 and 1 for two phonemes."""
    if p1 == p2:
        return 1.0  # Perfect match
    return PHONEME_SIMILARITY.get((p1, p2), PHONEME_SIMILARITY.get((p2, p1), 0.0))  # Check reverse
