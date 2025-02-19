from typing import Dict, Tuple


PHONEME_SIMILARITY: Dict[Tuple[str, str], float] = {
    # Plosives
    ("p", "b"): 0.8, ("t", "d"): 0.8, ("k", "ɡ"): 0.8,

    # Affricates
    ("tʃ", "dʒ"): 0.7,  # "ch" vs. "j" (close but distinct)
    
    # Fricatives
    ("f", "v"): 0.7, ("s", "z"): 0.7, ("ʃ", "ʒ"): 0.7, ("θ", "ð"): 0.7,  # Similar consonants
    ("x", "k"): 0.6,  # "kh" vs "k" (sometimes interchangeable)
    ("h", "hw"): 0.6,  # "h" vs. "wh" (aspiration similarity)

    # Nasals
    ("m", "n"): 0.6, ("n", "ŋ"): 0.7,  # "ng" close to "n"

    # Approximants
    ("l", "r"): 0.6, ("w", "v"): 0.6, ("j", "ɹ"): 0.6, ("j", "w"): 0.6,  # "y" vs. "r", "w"

    # Rhotics
    ("ɹ", "ɹ̩"): 0.9,  # "r" vs. "err"
    ("ər", "ɜːr"): 0.9, ("ɔːr", "ɑːr"): 0.8,  # "or" vs. "ar"

    # Vowels
    ("iː", "ɪ"): 0.8,  # "ee" vs. "i"
    ("eɪ", "ɛ"): 0.7,  # "ay" vs. "e"
    ("aɪ", "eɪ"): 0.6, ("aɪ", "ɪ"): 0.6,  # "y" vs. "ay" or "i"
    ("uː", "ʊ"): 0.8,  # "oo" vs. "uu"
    ("oʊ", "ɔː"): 0.8,  # "oh" vs. "aw"
    ("ɑː", "æ"): 0.7,  # "ah" vs. "a"
    ("ʌ", "ə"): 0.8,  # "u" vs. "uh"
    ("ɪər", "iː"): 0.7,  # "eer" vs. "ee"
    ("aʊ", "oʊ"): 0.7,  # "ow" vs. "oh"
    ("ɔɪ", "oʊ"): 0.6,  # "oy" vs. "oh"
    ("ʊər", "uː"): 0.7,  # "oor" vs. "oo"

    # Common reductions
    ("ə", "ɜːr"): 0.6, ("ə", "ʌ"): 0.7,  # "uh" and "u"
    ("ə", "iː"): 0.5, ("ə", "oʊ"): 0.5,  # "uh" close to "ee" or "oh" in some contexts
}
