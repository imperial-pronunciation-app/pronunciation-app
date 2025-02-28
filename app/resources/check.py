
import json


with open("word_data.json", "r") as f:
    word_data = json.load(f)
with open("phoneme_respellings.json", "r") as f:
    phoneme_respelling = json.load(f)

for word in word_data:
    phonemes = word["phonemes"]
    respellings = [phoneme_respelling.get(phoneme, phoneme + "? ") for phoneme in phonemes]
    print(f"Word: {word['word']}, Phonemes: {'.'.join(phonemes)}, Respellings: {'.'.join(respellings)}")