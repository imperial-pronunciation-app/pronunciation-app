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
import time
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
                time.sleep(1)  # Dont want to piss off the server (specified in the robots.txt)
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
    words = json.load(open("app/resources/new_words.json"))
    service = CrawlingService()
    service.get_phonemes_and_save(words)
