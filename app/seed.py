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
    {"word": "heat", "phonemes": ["h", "iː", "t"]}
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
            name="Short Vowel Sound",
            description="Focus on /æ/",
            order=1,
            lessons=[
                Lesson(title="Listening Discrimination Pairs", order=1, exercises=[
                    Exercise(index=0, word_id=words["cat"].id),
                    Exercise(index=1, word_id=words["cut"].id),
                    Exercise(index=2, word_id=words["hat"].id),
                    Exercise(index=3, word_id=words["hut"].id),
                    Exercise(index=4, word_id=words["bat"].id),
                    Exercise(index=5, word_id=words["bet"].id),
                    Exercise(index=6, word_id=words["pan"].id),
                    Exercise(index=7, word_id=words["pen"].id),
                ]),
                Lesson(title="Repetition Practice Words", order=2, exercises=[
                    Exercise(index=0, word_id=words["man"].id),
                    Exercise(index=1, word_id=words["bag"].id),
                    Exercise(index=2, word_id=words["cap"].id),
                    Exercise(index=3, word_id=words["sat"].id),
                    Exercise(index=4, word_id=words["dad"].id),
                    Exercise(index=5, word_id=words["jam"].id),
                    Exercise(index=6, word_id=words["map"].id),
                    Exercise(index=7, word_id=words["nap"].id),
                ])
            ]
            
        ),
        Unit(
            name="Consonant Sound",
            description="Focus on /p/",
            order=2,
            lessons=[
                Lesson(title="Sound Isolation Words", order=1, exercises=[
                    Exercise(index=0, word_id=words["pat"].id),
                    Exercise(index=1, word_id=words["pot"].id),
                    Exercise(index=2, word_id=words["pig"].id),
                    Exercise(index=3, word_id=words["pan"].id),
                    Exercise(index=4, word_id=words["pen"].id),
                    Exercise(index=5, word_id=words["pop"].id),
                    Exercise(index=6, word_id=words["pet"].id),
                    Exercise(index=7, word_id=words["pit"].id),
                ]),
                Lesson(title="Repetition Practice Words", order=2, exercises=[
                    Exercise(index=0, word_id=words["pen"].id),
                    Exercise(index=1, word_id=words["pin"].id),
                    Exercise(index=2, word_id=words["pack"].id),
                    Exercise(index=3, word_id=words["puff"].id),
                    Exercise(index=4, word_id=words["pit"].id),
                    Exercise(index=5, word_id=words["pair"].id),
                    Exercise(index=6, word_id=words["page"].id),
                    Exercise(index=7, word_id=words["pine"].id),
                ])
            ]
        ),
        Unit(
            name="Long Vowel Sound",
            description="Focus on /iː/",
            order=3,
            lessons=[
                Lesson(title="Listening Discrimination Pairs", order=1, exercises=[
                    Exercise(index=0, word_id=words["see"].id),
                    Exercise(index=1, word_id=words["sit"].id),
                    Exercise(index=2, word_id=words["feel"].id),
                    Exercise(index=3, word_id=words["fill"].id),
                    Exercise(index=4, word_id=words["sheep"].id),
                    Exercise(index=5, word_id=words["ship"].id),
                    Exercise(index=6, word_id=words["heel"].id),
                    Exercise(index=7, word_id=words["hill"].id),
                ]),
                Lesson(title="Repetition Practice Words", order=2, exercises=[
                    Exercise(index=0, word_id=words["tree"].id),
                    Exercise(index=1, word_id=words["keep"].id),
                    Exercise(index=2, word_id=words["tea"].id),
                    Exercise(index=3, word_id=words["free"].id),
                    Exercise(index=4, word_id=words["pea"].id),
                    Exercise(index=5, word_id=words["neat"].id),
                    Exercise(index=6, word_id=words["green"].id),
                    Exercise(index=7, word_id=words["heat"].id),
                ])
            ]
        ),
        Unit(
            name="Advanced Topics",
            description="More complex topics",
            order=4,
            lessons=[
                Lesson(title="Programming Terms", order=1, exercises=[
                    Exercise(index=0, word_id=words["compilers"].id),
                    Exercise(index=1, word_id=words["hardware"].id),
                    Exercise(index=2, word_id=words["software"].id)
                    ]),
                Lesson(title="Computer Accessories", order=2, exercises=[
                    Exercise(index=0, word_id=words["keyboard"].id),
                    Exercise(index=1, word_id=words["mouse"].id),
                    Exercise(index=2, word_id=words["computer"].id)
                    ]),
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
