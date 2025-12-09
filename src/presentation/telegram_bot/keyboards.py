from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.entities.Gender import Gender
from src.core.entities.GoalType import GoalType
from src.core.entities.TrainingExperience import TrainingExperience
from src.core.entities.TrainingStyle import TrainingStyle


def get_gender_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Мужской",
                callback_data=f"gender_{Gender.MALE.value}"
            ),
            InlineKeyboardButton(
                text="Женский",
                callback_data=f"gender_{Gender.FEMALE.value}"
            )
        ]
    ])

def get_goal_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Жим лежа 100 кг",
                callback_data=f"goal_{GoalType.BENCH_100KG.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Похудеть на 7 кг",
                callback_data=f"goal_{GoalType.LOSE_7KG.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Подтягиваться 12 раз",
                callback_data=f"goal_{GoalType.PULLUPS_12.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Набрать 4 кг мышечной массы",
                callback_data=f"goal_{GoalType.GAIN_4KG.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Свой вариант",
                callback_data=f"goal_{GoalType.CUSTOM.value}"
            )
        ]
    ])

def get_experience_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сейчас",
                callback_data=f"experience_{TrainingExperience.CURRENTLY.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="<3 месяца назад",
                callback_data=f"experience_{TrainingExperience.LESS_THAN_3_MONTHS.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="3-6 месяцев назад",
                callback_data=f"experience_{TrainingExperience.THREE_TO_SIX_MONTHS.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="6-12 месяцев назад",
                callback_data=f"experience_{TrainingExperience.SIX_TO_TWELVE_MONTHS.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Больше года назад",
                callback_data=f"experience_{TrainingExperience.MORE_THAN_YEAR.value}"
            )
        ]
    ])

def get_training_style_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Сбалансированный",
                callback_data=f"style_{TrainingStyle.BALANCED.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Силовой",
                callback_data=f"style_{TrainingStyle.STRENGTH.value}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Гипертрофия/Выносливость",
                callback_data=f"style_{TrainingStyle.HYPERTROPHY.value}"
            )
        ]
    ])