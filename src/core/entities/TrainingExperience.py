from enum import Enum


class TrainingExperience(str, Enum):
    CURRENTLY = "currently"
    LESS_THAN_3_MONTHS = "lt_3_months"
    THREE_TO_SIX_MONTHS = "3_6_months"
    SIX_TO_TWELVE_MONTHS = "6_12_months"
    MORE_THAN_YEAR = "gt_year"
