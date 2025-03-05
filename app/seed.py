import json
import os
import random
from typing import Any, Dict, List

from fastapi_users.password import PasswordHelper
from sqlmodel import Session, SQLModel, text

from app.database import engine
from app.models.analytics.analytics import EndpointAnalytics  # noqa: F401
from app.models.attempt import Attempt  # noqa: F401
from app.models.basic_lesson import BasicLesson  # noqa: F401
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt  # noqa: F401
from app.models.exercise_attempt_phoneme_link import ExerciseAttemptPhonemeLink  # noqa: F401
from app.models.language import Language
from app.models.leaderboard_user_link import LeaderboardUserLink, League  # noqa: F401
from app.models.lesson import Lesson
from app.models.phoneme import Phoneme
from app.models.phoneme_respelling import PhonemeRespelling
from app.models.recap_lesson import RecapLesson  # noqa: F401
from app.models.recording import Recording  # noqa: F401
from app.models.unit import Unit
from app.models.user import User
from app.models.word import Word
from app.models.word_of_day import WordOfDay
from app.models.word_of_day_attempt import WordOfDayAttempt  # noqa: F401
from app.models.word_phoneme_link import WordPhonemeLink
from app.redis import LRedis


class DatabaseSeeder:
    def __init__(self, session: Session, password_helper: PasswordHelper):
        self.session = session
        self.password_helper = password_helper

    def load_json_data(self, filepath: str) -> Dict[str, Any]:
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return json.load(file) # type: ignore
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading JSON from {filepath}: {e}")
            raise

    def seed_users(self, user_emails: List[str]) -> List[User]:
        print("👤 Inserting Users...")
        
        num_users = len(user_emails)
        xps = [random.randint(1000, 10000) for _ in range(num_users)]

        users = [
            User(
                email=email,
                display_name=" ".join(email.split("@")[0].split(".")).title(),
                hashed_password=self.password_helper.hash("password"),
                xp_total=xp,
            )
            for email, xp in zip(user_emails, xps)
        ]
        self.session.add_all(users)
        self.session.commit()

        return users

    def seed_leaderboard(self, users: List[User]) -> None:
        print("🏆 Inserting Leaderboard...")
        num_users = len(users)
        half_users = num_users // 2
        
        leagues = [League.BRONZE] * half_users + [League.SILVER] * (num_users - half_users)
        xps = [user.xp_total for user in users]
        
        leaderboard_users = [
            LeaderboardUserLink(user_id=user.id, xp=xp, league=league)
            for user, xp, league in zip(users, xps, leagues)
        ]
        
        self.session.add_all(leaderboard_users)
        self.session.commit()
        
        LRedis.clear()
        LRedis.create_entries_from_users(League.BRONZE, leaderboard_users[:half_users])
        LRedis.create_entries_from_users(League.SILVER, leaderboard_users[half_users:])

    def seed_languages(self, data_directory: str) -> None:
        print("🗂 Processing Language Data...")
        
        existing_phonemes: Dict[str, Phoneme] = {}

        for filename in sorted(os.listdir(data_directory)):
            if filename.endswith(".json"):
                filepath = os.path.join(data_directory, filename)
                self._seed_language(filepath, existing_phonemes)

    def _seed_language(self, filepath: str, existing_phonemes: Dict[str, Phoneme]) -> None:
        data = self.load_json_data(filepath)
        language_name = os.path.splitext(os.path.basename(filepath))[0]

        print(f"🌍 Inserting Language: {language_name}")
        language = Language(name=language_name)
        self.session.add(language)
        self.session.commit()

        self._seed_phonemes(data, language, existing_phonemes)

        words = self._seed_words(data, language)
        
        self._link_words_phonemes(data, words, existing_phonemes)

        self._seed_word_of_day(data, words)

        self._seed_units_and_lessons(data, language, words)

    def _seed_phonemes(self, data: Dict, language: Language, existing_phonemes: Dict[str, Phoneme]) -> None:
        print("🔤 Adding Phoneme Respellings...")
        phoneme_respellings = []
        
        for ipa, content in data["respellings"].items():
            respelling, cdn_path = content
            if ipa not in existing_phonemes:
                phoneme = Phoneme(ipa=ipa, cdn_path=cdn_path)
                self.session.add(phoneme)
                self.session.commit()
                existing_phonemes[ipa] = phoneme

            phoneme_respellings.append(
                PhonemeRespelling(
                    phoneme_id=existing_phonemes[ipa].id, 
                    language_id=language.id, 
                    respelling=respelling
                )
            )

        self.session.add_all(phoneme_respellings)
        self.session.commit()

    def _seed_words(self, data: Dict, language: Language) -> Dict[str, Word]:
        print("📝 Inserting Words...")
        words = {word: Word(text=word, language_id=language.id) for word in data["words"].keys()}
        self.session.add_all(words.values())
        self.session.commit()
        return words

    def _link_words_phonemes(self, data: Dict, words: Dict[str, Word], existing_phonemes: Dict[str, Phoneme]) -> None:
        print("🔗 Linking Words and Phonemes...")
        word_phoneme_links = []
        
        for word_text, phoneme_list in data["words"].items():
            word_obj = words[word_text]
            for index, ipa in enumerate(phoneme_list):
                if ipa not in existing_phonemes:
                    raise ValueError(f"Phoneme {ipa} not found for word {word_text}")
                
                word_phoneme_links.append(
                    WordPhonemeLink(
                        word_id=word_obj.id, 
                        phoneme_id=existing_phonemes[ipa].id, 
                        index=index
                    )
                )

        self.session.add_all(word_phoneme_links)
        self.session.commit()

    def _seed_word_of_day(self, data: Dict, words: Dict[str, Word]) -> None:
        print("📅 Inserting Word of the Day...")
        word_of_day_word = words[data["word_of_day"]]
        word_of_day = WordOfDay(word_id=word_of_day_word.id)
        word_of_day_word.word_of_day_last_used = word_of_day.date
        
        self.session.add(word_of_day)
        self.session.commit()

    def _seed_units_and_lessons(self, data: Dict, language: Language, words: Dict[str, Word]) -> None:
        print("📚 Inserting Units with Lessons...")

        for index, unit_data in enumerate(data["units"]):
            unit = Unit(
                name=unit_data["name"],
                description=unit_data["description"],
                index=index,
                language_id=language.id,
            )
            self.session.add(unit)
            self.session.commit()

            for index, lesson_data in enumerate(unit_data["lessons"]):
                lesson =  Lesson(
                    title=lesson_data["title"], 
                    exercises=[
                        Exercise(index=i, word_id=words[word].id) 
                        for i, word in enumerate(lesson_data["exercises"])
                    ]
                )

                self.session.add(lesson)
                self.session.commit()

                basic_lesson = BasicLesson(
                    id=lesson.id,
                    index=index,
                    unit_id=unit.id
                )
                
                self.session.add(basic_lesson)
                self.session.commit()

def seed_database(user_emails: List[str], data_directory: str) -> None:
    """Main seeding function."""
    print("🔄 Resetting database schema...")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    
    SQLModel.metadata.create_all(engine)
    
    password_helper = PasswordHelper()
    
    with Session(engine) as session:
        seeder = DatabaseSeeder(session, password_helper)
        
        try:
            users = seeder.seed_users(user_emails)
            seeder.seed_leaderboard(users)
            seeder.seed_languages(data_directory)
            print("🎉✅ Database seeding completed successfully!")
        except Exception as e:
            print(f"Seeding failed: {e}")
            session.rollback()
            raise

if __name__ == "__main__":
    user_emails = [
        "john.doe@example.com",
        "emma.smith@example.com",
        "liam.johnson@example.com",
        "olivia.brown@example.com",
        "noah.williams@example.com",
        "ava.jones@example.com",
        "sophia.miller@example.com",
        "mason.davis@example.com",
        "isabella.garcia@example.com",
        "logan.martinez@example.com",
        "lucas.anderson@example.com",
        "mia.thomas@example.com",
        "harper.taylor@example.com",
        "elijah.moore@example.com",
        "amelia.white@example.com",
        "james.harris@example.com",
        "charlotte.clark@example.com",
        "benjamin.lewis@example.com",
        "henry.walker@example.com",
        "evelyn.hall@example.com",
    ]

    seed_database(user_emails, "data/languages")
