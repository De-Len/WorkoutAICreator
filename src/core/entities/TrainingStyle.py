from enum import Enum


class TrainingStyle(str, Enum):
    BALANCED = "balanced"
    STRENGTH = "strength"
    HYPERTROPHY = "hypertrophy"