from .attempt_admin import AttemptAdmin
from .exercise_admin import ExerciseAdmin
from .leaderboard_user_link_admin import LeaderboardUserLinkAdmin
from .lesson_admin import LessonAdmin
from .phoneme_admin import PhonemeAdmin
from .recording_admin import RecordingAdmin
from .unit_admin import UnitAdmin
from .user_admin import UserAdmin
from .word_admin import WordAdmin
from .word_phoneme_link_admin import WordPhonemeLinkAdmin


views = sorted([
    AttemptAdmin,
    ExerciseAdmin,
    LeaderboardUserLinkAdmin,
    LessonAdmin,
    PhonemeAdmin,
    RecordingAdmin,
    UnitAdmin,
    UserAdmin,
    WordAdmin,
    WordPhonemeLinkAdmin,
], key=lambda x: x.__name__)
