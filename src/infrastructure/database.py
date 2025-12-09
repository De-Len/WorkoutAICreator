from sqlalchemy import Column, String, Integer, Text, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///./fitness.db")  # Или из config
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(String, nullable=True, index=True)
    session_id = Column(String, unique=True, index=True)

    # Шаг 1
    gender = Column(String)
    age = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)

    # Шаг 2
    goal = Column(String)
    custom_goal = Column(Text, nullable=True)
    months = Column(Integer)

    # Шаг 3
    current_results = Column(Text)
    last_trained = Column(String)

    # Шаг 4
    workouts_per_week = Column(Integer)
    workout_duration = Column(Integer)
    training_style = Column(String)

    # Шаг 5
    health_restrictions = Column(Text)
    preferences = Column(Text)

    # Результат
    generated_program = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TrainingProgramModel(Base):
    __tablename__ = "training_programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_profile_id = Column(UUID(as_uuid=True), index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)