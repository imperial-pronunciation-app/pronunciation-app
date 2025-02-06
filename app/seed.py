import json
from typing import List, TypedDict

from fastapi_users.password import PasswordHelper
from sqlmodel import Session, SQLModel, text

from app.database import engine
from app.models.attempt import Attempt  # noqa: F401
from app.models.exercise import Exercise
from app.models.leaderboard_user_link import LeaderboardUserLink  # noqa: F401
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.recording import Recording  # noqa: F401
from app.models.unit import Unit
from app.models.user import User
from app.models.word import Word
from app.models.word_phoneme_link import WordPhonemeLink
from app.redis import LRedis


password_helper = PasswordHelper()

with open("app/resources/phoneme_respellings.json") as f:
    ipa_to_respelling = json.load(f)

class WordEntry(TypedDict):
    word: str
    phonemes: List[str]

word_data: List[WordEntry] = [
    {"word": "software", "phonemes": ["s", "oʊ", "f", "t", "w", "ɛ", "r"]},
    {"word": "hardware", "phonemes": ["h", "ɑː", "r", "d", "w", "ɛ", "r"]},
    {"word": "computer", "phonemes": ["k", "ə", "m", "p", "j", "uː", "t", "ə"]},
    {"word": "compilers", "phonemes": ["k", "ə", "m", "p", "aɪ", "l", "ə", "r"]},
    {"word": "keyboard", "phonemes": ["k", "iː", "b", "ɔː", "d"]},
    {"word": "mouse", "phonemes": ["m", "aʊ", "s"]},
    {"word": "parrot", "phonemes": ["p", "æ", "r", "ə", "t"]},
    {"word": "chocolate", "phonemes": ["tʃ", "ɒ", "k", "l", "ə", "t"]},
]

def seed(session: Session) -> None:
    print("👤 Inserting Users...")
    users = [
        User(email="user1@example.com", hashed_password=password_helper.hash("password")),
        User(email="user2@example.com", hashed_password=password_helper.hash("password"))
    ]
    session.add_all(users)
    session.commit()

    print("📝 Inserting Words...")
    words = {w["word"]: Word(text=w["word"]) for w in word_data}
    session.add_all(words.values())
    session.commit()

    print("🔤 Inserting Phonemes...")
    phonemes = {ipa: Phoneme(ipa=ipa, respelling=respelling) for ipa, respelling in ipa_to_respelling.items()}
    session.add_all(phonemes.values())
    session.commit()

    print("🔗 Linking Words and Phonemes...")
    word_phoneme_links = []
    for word_entry in word_data:
        word_obj = words[word_entry["word"]]
        for index, ipa in enumerate(word_entry["phonemes"]):
            word_phoneme_links.append(WordPhonemeLink(
                word_id=word_obj.id,
                phoneme_id=phonemes[ipa].id,
                index=index
            ))
    session.add_all(word_phoneme_links)
    session.commit()

    print("📚 Inserting Units with Lessons...")
    units = [
        Unit(
            name="Basic Phonemes",
            description="Introduction to phonemes",
            order=1,
            lessons=[
                Lesson(title="Short Vowels", order=1, exercises=[Exercise(index=0, word_id=words["software"].id)]),
                Lesson(title="Long Vowels", order=2, exercises=[Exercise(index=0, word_id=words["hardware"].id)])
            ]
        ),
        Unit(
            name="Common Words",
            description="Practicing everyday words",
            order=2,
            lessons=[
                Lesson(title="Common Nouns", order=1, exercises=[Exercise(index=0, word_id=words["computer"].id)])
            ]
        )
    ]
    session.add_all(units)
    session.commit()
    LRedis.clear()

    print("🎉✅ Database seeding completed successfully!")

# To seed inside a container
# docker exec -it <container_id> python -m app.seed
if __name__ == "__main__":
    print("🔄 Resetting database schema...")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    SQLModel.metadata.create_all(engine)
    seed(Session(engine))
