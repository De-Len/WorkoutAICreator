from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from src.core.entities.Gender import Gender
from src.core.entities.GoalType import GoalType
from src.core.entities.TrainingExperience import TrainingExperience
from src.core.entities.TrainingStyle import TrainingStyle


# DTO для входящих данных
class UserProfileStep1DTO(BaseModel):
    gender: Gender
    age: int = Field(ge=10, le=100)
    height: int = Field(ge=100, le=250)
    weight: int = Field(ge=30, le=200)

class UserProfileStep2DTO(BaseModel):
    goal: GoalType
    custom_goal: Optional[str] = None
    months: int = Field(ge=1, le=24)

class UserProfileStep3DTO(BaseModel):
    current_results: str = Field(min_length=1, max_length=1000)
    last_trained: TrainingExperience

class UserProfileStep4DTO(BaseModel):
    workouts_per_week: int = Field(ge=1, le=7)
    workout_duration: int = Field(ge=15, le=180)
    training_style: TrainingStyle

class UserProfileStep5DTO(BaseModel):
    health_restrictions: str = Field(min_length=1, max_length=1000)
    preferences: str = Field(min_length=1, max_length=1000)

class CreateUserProfileDTO(BaseModel):
    telegram_id: Optional[str] = None
    session_id: str

# DTO для исходящих данных
class UserProfileResponseDTO(BaseModel):
    id: UUID
    telegram_id: Optional[str]
    is_complete: bool
    created_at: datetime
    updated_at: datetime

class TrainingProgramResponseDTO(BaseModel):
    id: UUID
    user_profile_id: UUID
    content: str
    created_at: datetime

class GenerateProgramRequestDTO(BaseModel):
    session_id: str