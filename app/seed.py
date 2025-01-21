from dataclasses import dataclass
from typing import List

from sqlmodel import Session

from app.models import Phoneme, Word, WordPhonemeLink


# Maps IPA characters to Wiki respellings
ipa_to_respelling = {
    "tʃ": "ch",
    "ɡ": "g",
    "h": "h",
    "hw": "wh",
    "dʒ": "j",
    "k": "k",
    "x": "kh",
    "ŋ": "ng",
    "s": "s",
    "ʃ": "sh",
    "θ": "th",
    "ð": "dh",
    "j": "y",
    "ʒ": "zh",
    "b": "b",
    "d": "d",
    "f": "f",
    "l": "l",
    "m": "m",
    "n": "n",
    "p": "p",
    "r": "r",
    "t": "t",
    "v": "v",
    "w": "w",
    "z": "z",
    "æ": "a (arr)",
    "eɪ": "ay",
    "ɛər": "air",
    "ɑː": "ah",
    "ɑːr": "ar",
    "ɛ": "e (err)",
    "i:": "ee",
    "ɪər": "eer",
    "ɪ": "i (irr)",
    "aɪ": "y, eye",
    "ɒ": "o (orr)",
    "oʊ": "oh",
    "ɔː": "aw",
    "ɔːr": "or",
    "ɔɪ": "oy",
    "ʊ": "uu",
    "ʊər": "oor",
    "u:": "oo",
    "aʊ": "ow",
    "ʌ": "u",
    "ɜːr": "ur",
    "ə": "ə",  # I think the Mac respelling of uh for this and the next is better
    "ər": "ər",
    "ju:": "ew",
}

@dataclass
class WordData:
    word: str
    phonemes: List[str] # ordered list of IPA phonemes

    def __str__(self) -> str:
        """String representation for pytest parameter IDs
        """
        return f"{self.word}: {'-'.join(self.phonemes)}"

@dataclass
class SeedData:
    """Container for specific seed configuration
    """
    words: List[WordData]
    
    def __str__(self) -> str:
        """String representation for pytest parameter IDs
        """
        return "_".join([str(word) for word in self.words])

def seed_data(session: Session, seed_words: SeedData) -> None:
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
