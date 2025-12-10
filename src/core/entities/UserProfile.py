from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from src.core.entities.Gender import Gender
from src.core.entities.GoalType import GoalType
from src.core.entities.TrainingExperience import TrainingExperience
from src.core.entities.TrainingStyle import TrainingStyle


@dataclass
class UserProfile:
    """Доменная сущность: Профиль пользователя"""
    id: UUID = field(default_factory=uuid4)
    telegram_id: Optional[str] = None

    # Шаг 1
    gender: Optional[Gender] = None
    age: Optional[int] = None
    height: Optional[int] = None  # см
    weight: Optional[int] = None  # кг

    # Шаг 2
    goal: Optional[GoalType] = None
    custom_goal: Optional[str] = None
    months: Optional[int] = None

    # Шаг 3
    current_results: Optional[str] = None
    last_trained: Optional[TrainingExperience] = None

    # Шаг 4
    workouts_per_week: Optional[int] = None
    workout_duration: Optional[int] = None  # минуты
    training_style: Optional[TrainingStyle] = None

    # Шаг 5
    health_restrictions: Optional[str] = None
    preferences: Optional[str] = None

    # Результат
    generated_program: Optional[str] = None

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update(self, **kwargs):
        """Обновление профиля"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def is_complete(self) -> bool:
        """Проверка, заполнен ли профиль полностью"""
        # Обязательные поля (не могут быть пустыми)
        required_fields = [
            self.gender, self.age, self.height, self.weight,
            self.goal, self.months,
            self.current_results, self.last_trained,
            self.workouts_per_week, self.workout_duration, self.training_style
        ]

        # health_restrictions и preferences могут быть пустыми
        # но должны быть установлены (не None)
        optional_but_required_fields = [
            self.health_restrictions,
            self.preferences
        ]

        # Все обязательные поля должны быть не None
        all_required = all(field is not None for field in required_fields)

        # Опциональные поля должны быть не None (но могут быть пустыми строками)
        all_optional = all(field is not None for field in optional_but_required_fields)

        return all_required and all_optional