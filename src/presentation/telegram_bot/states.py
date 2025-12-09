from aiogram.fsm.state import State, StatesGroup


class UserProfileStates(StatesGroup):
    waiting_gender = State()
    waiting_age = State()
    waiting_height = State()
    waiting_weight = State()

    waiting_goal = State()
    waiting_custom_goal = State()
    waiting_months = State()

    waiting_current_results = State()
    waiting_last_trained = State()

    waiting_workouts_per_week = State()
    waiting_workout_duration = State()
    waiting_training_style = State()

    waiting_health_restrictions = State()
    waiting_preferences = State()