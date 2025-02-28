# Contains routes and endpoints
from .attempts import router as attempts_router
from .auth import router as auth_router
from .leaderboard import router as leaderboard_router
from .lessons import router as lessons_router
from .units import router as units_router
from .users import router as users_router
from .word_of_day import router as word_of_day_router


routers = [
    auth_router,
    leaderboard_router,
    attempts_router,
    users_router,
    lessons_router,
    units_router,
    word_of_day_router,
]
