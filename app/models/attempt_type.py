from enum import Enum


class AttemptType(str, Enum):
    CONTINUAL = "continual"
    EXERCISE = "exercise"
    WOTD = "wotd"
