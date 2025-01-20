from sqlmodel import Session, create_engine

from app.models import Phoneme, Word, WordPhonemes

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
    # "'a": "A", # TODO: stressed syllables need to be handled
    # "ˌa": "A",
    # "a": "a",
}


def seed_data(database_url: str):
    engine = create_engine(database_url, echo=True)

    with Session(engine) as session:
        # Create sample phonemes
        phonemes = [Phoneme(ipa=ipa, respelling=respelling) for ipa, respelling in ipa_to_respelling.items()]
        session.add_all(phonemes)
        # Create sample words
        words = [Word(id=1, text="software"), Word(id=2, text="hardware")]
        session.add_all(words)

        # Create a dictionary to map IPA to Phoneme objects
        ipa_to_phoneme = {phoneme.ipa: phoneme for phoneme in phonemes}

        # Create sample word phonemes
        word_phonemes = [
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["s"].id, index=0),
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["oʊ"].id, index=1),
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["f"].id, index=2),
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["t"].id, index=3),
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["w"].id, index=4),
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["ɛ"].id, index=5),
            WordPhonemes(word_id=1, phoneme_id=ipa_to_phoneme["r"].id, index=6),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["h"].id, index=0),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["ɑː"].id, index=1),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["r"].id, index=2),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["d"].id, index=3),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["w"].id, index=4),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["ɛ"].id, index=5),
            WordPhonemes(word_id=2, phoneme_id=ipa_to_phoneme["r"].id, index=6),
        ]
        session.add_all(word_phonemes)

    session.commit()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python seed.py <DATABASE_URL>")
        sys.exit(1)
    database_url = sys.argv[1]
    seed_data(database_url)
    print("Database seeded successfull!")
