# Contains routes and endpoints
from .auth import router as auth_router
from .leaderboard import router as leaderboard_router
from .random_word import router as random_word_router
from .recording import router as recording_router
from .units import router as units_router
from .users import router as users_router


routers = [
    auth_router,
    leaderboard_router,
    random_word_router,
    recording_router,
    users_router,
    units_router
]
