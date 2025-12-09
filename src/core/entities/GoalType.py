from enum import Enum


class GoalType(str, Enum):
    BENCH_100KG = "bench_100kg"
    LOSE_7KG = "lose_7kg"
    PULLUPS_12 = "pullups_12"
    GAIN_4KG = "gain_4kg"
    CUSTOM = "custom"