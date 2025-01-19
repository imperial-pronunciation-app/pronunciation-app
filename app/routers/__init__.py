# Contains routes and endpoints

# TODO: Would we rather just have one router with all the endpoints?
from .random_word import router as random_word_router
from .recording import router as recording_router
from .satisfaction import router as satisfaction_router

__all__ = [
    "random_word_router",
    "recording_router",
    "satisfaction_router",
]
