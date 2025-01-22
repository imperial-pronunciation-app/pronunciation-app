from sqlmodel import Session

from app.models import Phoneme, Word, WordPhonemeLink
from app.seed_data import SeedData, ipa_to_respelling


def seed(session: Session, seed_words: SeedData) -> None:
    """Seed a database with sample data

    Args:
        session (Session): Session for database
        seed_data (SeedData): Words and their phonemes to seed
    """

    # Seed phonemes (no stressed phonemes)
    seed_phonemes = [Phoneme(ipa=ipa, respelling=respelling) for ipa, respelling in ipa_to_respelling.items()]
    session.add_all(seed_phonemes)
    
    # Seed specified words, retain phonemes to make seeding the links easier
    word_phonemes = [(Word(word=word_data.word), word_data.phonemes) for word_data in seed_words.words]
    session.add_all([word for word, _ in word_phonemes])
    
    session.commit() # Get IDs

    # Map IPA characters to Phoneme objects
    ipa_to_phoneme = {phoneme.ipa: phoneme for phoneme in seed_phonemes}

    # Seed word phoneme links
    word_phoneme_links = []
    for word, phonemes in word_phonemes:
        word_id = word.id
        for i, ipa in enumerate(phonemes):
            phoneme_id = ipa_to_phoneme[ipa].id
            word_phoneme_links.append(WordPhonemeLink(word_id=word_id, phoneme_id=phoneme_id, index=i))

    session.add_all(word_phoneme_links)

    session.commit()
