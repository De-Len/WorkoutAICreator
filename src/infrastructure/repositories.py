from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.core.entities.Gender import Gender
from src.core.entities.GoalType import GoalType
from src.core.entities.TrainingExperience import TrainingExperience
from src.core.entities.TrainingProgram import TrainingProgram
from src.core.entities.TrainingStyle import TrainingStyle
from src.core.entities.UserProfile import UserProfile
from src.core.interfaces.TrainingProgramRepository import TrainingProgramRepository
from src.core.interfaces.UserProfileRepository import UserProfileRepository
from src.infrastructure.database import UserProfileModel, TrainingProgramModel


class SQLAlchemyUserProfileRepository(UserProfileRepository):
    """Реализация репозитория профилей на SQLAlchemy"""

    def __init__(self, session: Session):
        self.session = session

    async def get_by_id(self, profile_id: UUID) -> Optional[UserProfile]:
        model = self.session.query(UserProfileModel).filter_by(id=profile_id).first()
        return self._to_domain(model) if model else None

    async def get_by_telegram_id(self, telegram_id: str) -> Optional[UserProfile]:
        model = self.session.query(UserProfileModel).filter_by(telegram_id=telegram_id).first()
        return self._to_domain(model) if model else None

    async def get_by_session_id(self, session_id: str) -> Optional[UserProfile]:
        model = self.session.query(UserProfileModel).filter_by(session_id=session_id).first()
        return self._to_domain(model) if model else None

    async def save(self, profile: UserProfile) -> UserProfile:
        model = self._to_model(profile)
        self.session.add(model)
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

        return self._to_domain(model)

    async def update(self, profile: UserProfile) -> UserProfile:
        model = self.session.query(UserProfileModel).filter_by(id=profile.id).first()
        if not model:
            raise ValueError(f"Profile {profile.id} not found")

        # Обновление полей
        for field in ['gender', 'age', 'height', 'weight', 'goal', 'custom_goal',
                      'months', 'current_results', 'last_trained', 'workouts_per_week',
                      'workout_duration', 'training_style', 'health_restrictions',
                      'preferences', 'generated_program', 'telegram_id', 'session_id']:
            if hasattr(profile, field):
                setattr(model, field, getattr(profile, field))

        model.updated_at = profile.updated_at
        self.session.commit()

        return self._to_domain(model)

    def _to_model(self, profile: UserProfile) -> UserProfileModel:
        """Конвертация доменной сущности в модель БД"""
        return UserProfileModel(
            id=profile.id,
            telegram_id=profile.telegram_id,
            session_id=str(profile.id),  # Используем ID как session_id
            gender=profile.gender.value if profile.gender else None,
            age=profile.age,
            height=profile.height,
            weight=profile.weight,
            goal=profile.goal.value if profile.goal else None,
            custom_goal=profile.custom_goal,
            months=profile.months,
            current_results=profile.current_results,
            last_trained=profile.last_trained.value if profile.last_trained else None,
            workouts_per_week=profile.workouts_per_week,
            workout_duration=profile.workout_duration,
            training_style=profile.training_style.value if profile.training_style else None,
            health_restrictions=profile.health_restrictions,
            preferences=profile.preferences,
            generated_program=profile.generated_program,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    def _to_domain(self, model: UserProfileModel) -> UserProfile:
        """Конвертация модели БД в доменную сущность"""
        return UserProfile(
            id=model.id,
            telegram_id=model.telegram_id,
            gender=Gender(model.gender) if model.gender else None,
            age=model.age,
            height=model.height,
            weight=model.weight,
            goal=GoalType(model.goal) if model.goal else None,
            custom_goal=model.custom_goal,
            months=model.months,
            current_results=model.current_results,
            last_trained=TrainingExperience(model.last_trained) if model.last_trained else None,
            workouts_per_week=model.workouts_per_week,
            workout_duration=model.workout_duration,
            training_style=TrainingStyle(model.training_style) if model.training_style else None,
            health_restrictions=model.health_restrictions,
            preferences=model.preferences,
            generated_program=model.generated_program,
            created_at=model.created_at,
            updated_at=model.updated_at
        )


class SQLAlchemyTrainingProgramRepository(TrainingProgramRepository):
    """Реализация репозитория программ тренировок на SQLAlchemy"""

    def __init__(self, session: Session):
        self.session = session

    async def save(self, program: TrainingProgram) -> TrainingProgram:
        model = TrainingProgramModel(
            id=program.id,
            user_profile_id=program.user_profile_id,
            content=program.content,
            created_at=program.created_at
        )
        self.session.add(model)
        self.session.commit()
        return program

    async def get_by_user_profile(self, profile_id: UUID) -> List[TrainingProgram]:
        models = self.session.query(TrainingProgramModel).filter_by(
            user_profile_id=profile_id
        ).all()

        return [
            TrainingProgram(
                id=model.id,
                user_profile_id=model.user_profile_id,
                content=model.content,
                created_at=model.created_at
            )
            for model in models
        ]