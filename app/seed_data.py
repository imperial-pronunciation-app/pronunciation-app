

# Maps IPA characters to Wiki respellings
import json
from dataclasses import dataclass
from typing import List


with open("app/resources/phoneme_respellings.json") as f:
    ipa_to_respelling = json.load(f)

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
        WordData(word="computer", phonemes=["k", "ə", "m", "p", "j", "uː", "t", "ə"]),
        WordData(word="compilers", phonemes=["k", "ə", "m", "p", "aɪ", "l", "ə", "r"]),
        WordData(word="keyboard", phonemes=["k", "iː", "b", "ɔː", "d"]),
        WordData(word="mouse", phonemes=["m", "aʊ", "s"]),
        WordData(word="parrot", phonemes=["p", "æ", "r", "ə", "t"]),
        WordData(word="chocolate", phonemes=["tʃ", "ɒ", "k", "l", "ə", "t"]),
    ])