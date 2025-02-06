from .leaderboard_user_admin import LeaderboardUserAdmin
from .phoneme_admin import PhonemeAdmin
from .recording_admin import RecordingAdmin
from .user_admin import UserAdmin
from .word_admin import WordAdmin
from .word_phoneme_link_admin import WordPhonemeLinkAdmin


views = sorted([
    LeaderboardUserAdmin,
    PhonemeAdmin,
    RecordingAdmin,
    UserAdmin,
    WordAdmin,
    WordPhonemeLinkAdmin,
], key=lambda x: x.__name__)
