

# Maps IPA characters to Wiki respellings
from dataclasses import dataclass
from typing import List


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

default_data = SeedData(words=[
        WordData(word="software", phonemes=["s", "oʊ", "f", "t", "w", "ɛ", "r"]),
        WordData(word="hardware", phonemes=["h", "ɑː", "r", "d", "w", "ɛ", "r"]),
        WordData(word="computer", phonemes=["k", "ə", "m", "p", "j", "u:", "t", "ə"]),
        WordData(word="compilers", phonemes=["k", "ə", "m", "p", "aɪ", "l", "ə", "r"]),
        WordData(word="keyboard", phonemes=["k", "i:", "b", "ɔː", "d"]),
        WordData(word="mouse", phonemes=["m", "aʊ", "s"]),
        WordData(word="parrot", phonemes=["p", "æ", "r", "ə", "t"]),
        WordData(word="chocolate", phonemes=["tʃ", "ɒ", "k", "l", "ə", "t"]),
    ])