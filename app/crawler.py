"""
Abstract:
This module is responsible for crawling the Cambridge Dictionary website to get the phonemes of a list of words.

1. Run the script to get the phonemes of the words in the new_words.json file.
2. The phonemes are saved in the word_data.json file in the resources folder.

Output format:

word_data: List[WordEntry] = [
    {"word": "software", "phonemes": ["s", "oʊ", "f", "t", "w", "ɛ", "r"]},
    {"word": "heat", "phonemes": ["h", "iː", "t"]},

]
"""

import json
from typing import List, TypedDict

import requests
from bs4 import BeautifulSoup


# This is the same as the WordEntry class in the app/seed.py file
# Redefined here to allow for this script to run independently, outside of docker
class WordEntry(TypedDict):
    word: str
    phonemes: List[str]


class CrawlingService:
    def __init__(self) -> None:
        self.mappings: dict = json.load(open("app/resources/ipa_to_phoneme.json"))
        self.url = "https://dictionary.cambridge.org/pronunciation/english/"
        # We need to fake that we are a browser otherwise we get blocked :/
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _ipa_to_phonemes(self, ipa: str) -> list:
        # Apply the mappings
        for key, value in self.mappings.items():
            ipa = ipa.replace(key, value)

        phonemes_list = []
        i = 0
        while i < len(ipa):
            # Keep paired phonemes together
            if ipa[i : i + 2] in self.mappings.values():
                phonemes_list.append(ipa[i : i + 2])
                i += 2
            else:
                # 'e' edge case
                if ipa[i] == "e":
                    phonemes_list.append("ɛ")
                    i += 1
                else:
                    phonemes_list.append(ipa[i])
                    i += 1

        return phonemes_list

    def crawler_words(self, words: list) -> list[WordEntry]:
        ipa_data = []
        for word in words:
            try:
                res = requests.get(self.url + word, headers=self.headers)
                bs4 = BeautifulSoup(res.text, "html.parser")
                ipa = bs4.find("span", class_="ipa").text
                ipa_data.append({"word": word, "ipa": ipa})
                # time.sleep(1)  # Dont want to piss off the server (specified in the robots.txt)
            except requests.exceptions.RequestException as e:
                print(e)

        # Transform the gathered words into the desired format
        word_data = []
        for data in ipa_data:
            phonemes = self._ipa_to_phonemes(data["ipa"])
            word_data.append(WordEntry(word=data["word"], phonemes=phonemes))
        return word_data

    def get_phonemes_and_save(self, words: list, save_method: str = "w") -> None:
        if save_method != "w" and save_method != "a":
            raise ValueError("save_method must be either 'w' or 'a'")

        phonemes = self.crawler_words(words)
        with open("app/resources/word_data.json", save_method) as f:
            json.dump(phonemes, f, indent=4)
        print("""
              _______________________________________________________
              |                                                     |
              |     Data saved to app/resources/word_data.json      |
              |_____________________________________________________|
              """)


if __name__ == "__main__":
    # words = json.load(open("app/resources/new_words.json"))
    # service = CrawlingService()
    # service.get_phonemes_and_save(words)
    phonemes = [
        {"word": "software", "phonemes": ["s", "oʊ", "f", "t", "w", "ɛ", "r"]},
        {"word": "hardware", "phonemes": ["h", "ɑː", "ɹ", "d", "w", "ɛ", "ɹ"]},
        {"word": "computer", "phonemes": ["k", "ə", "m", "p", "j", "uː", "t", "ə"]},
        {"word": "compilers", "phonemes": ["k", "ə", "m", "p", "aɪ", "l", "ə", "r"]},
        {"word": "keyboard", "phonemes": ["k", "iː", "b", "ɔː", "d"]},
        {"word": "mouse", "phonemes": ["m", "aʊ", "s"]},
        {"word": "parrot", "phonemes": ["p", "æ", "r", "ə", "t"]},
        {"word": "chocolate", "phonemes": ["tʃ", "ɒ", "k", "l", "ə", "t"]},
        {"word": "cat", "phonemes": ["k", "æ", "t"]},
        {"word": "cut", "phonemes": ["k", "ʌ", "t"]},
        {"word": "hat", "phonemes": ["h", "æ", "t"]},
        {"word": "hut", "phonemes": ["h", "ʌ", "t"]},
        {"word": "bat", "phonemes": ["b", "æ", "t"]},
        {"word": "bet", "phonemes": ["b", "ɛ", "t"]},
        {"word": "pan", "phonemes": ["p", "æ", "n"]},
        {"word": "pen", "phonemes": ["p", "ɛ", "n"]},
        {"word": "man", "phonemes": ["m", "æ", "n"]},
        {"word": "bag", "phonemes": ["b", "æ", "ɡ"]},
        {"word": "cap", "phonemes": ["k", "æ", "p"]},
        {"word": "sat", "phonemes": ["s", "æ", "t"]},
        {"word": "dad", "phonemes": ["d", "æ", "d"]},
        {"word": "jam", "phonemes": ["dʒ", "æ", "m"]},
        {"word": "map", "phonemes": ["m", "æ", "p"]},
        {"word": "nap", "phonemes": ["n", "æ", "p"]},
        {"word": "pat", "phonemes": ["p", "æ", "t"]},
        {"word": "pot", "phonemes": ["p", "ɒ", "t"]},
        {"word": "pig", "phonemes": ["p", "ɪ", "ɡ"]},
        {"word": "pop", "phonemes": ["p", "ɒ", "p"]},
        {"word": "pet", "phonemes": ["p", "ɛ", "t"]},
        {"word": "pit", "phonemes": ["p", "ɪ", "t"]},
        {"word": "pin", "phonemes": ["p", "ɪ", "n"]},
        {"word": "pack", "phonemes": ["p", "æ", "k"]},
        {"word": "puff", "phonemes": ["p", "ʌ", "f"]},
        {"word": "pair", "phonemes": ["p", "ɛ", "ə", "ɹ"]},
        {"word": "page", "phonemes": ["p", "eɪ", "dʒ"]},
        {"word": "pine", "phonemes": ["p", "aɪ", "n"]},
        {"word": "see", "phonemes": ["s", "iː"]},
        {"word": "sit", "phonemes": ["s", "ɪ", "t"]},
        {"word": "feel", "phonemes": ["f", "iː", "l"]},
        {"word": "fill", "phonemes": ["f", "ɪ", "l"]},
        {"word": "sheep", "phonemes": ["ʃ", "iː", "p"]},
        {"word": "ship", "phonemes": ["ʃ", "ɪ", "p"]},
        {"word": "heel", "phonemes": ["h", "iː", "l"]},
        {"word": "hill", "phonemes": ["h", "ɪ", "l"]},
        {"word": "tree", "phonemes": ["t", "r", "iː"]},
        {"word": "keep", "phonemes": ["k", "iː", "p"]},
        {"word": "tea", "phonemes": ["t", "iː"]},
        {"word": "free", "phonemes": ["f", "r", "iː"]},
        {"word": "pea", "phonemes": ["p", "iː"]},
        {"word": "neat", "phonemes": ["n", "iː", "t"]},
        {"word": "green", "phonemes": ["ɡ", "r", "iː", "n"]},
        {"word": "heat", "phonemes": ["h", "iː", "t"]},
    ]

    with open("app/resources/test.json", "w") as f:
        json.dump(phonemes, f, indent=4)
    print("""
              _______________________________________________________
              |                                                     |
              |     Data saved to app/resources/word_data.json      |
              |_____________________________________________________|
              """)
    
    print(json.load(open("app/resources/word_data.json")))
