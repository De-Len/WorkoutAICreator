from sqlalchemy.orm import Session
from src.infrastructure.database import Base, engine, SessionLocal
from src.infrastructure.repositories import (
    SQLAlchemyUserProfileRepository,
    SQLAlchemyTrainingProgramRepository
)


class UnitOfWork:
    """Unit of Work паттерн для управления транзакциями"""

    def __init__(self):
        self.session: Session = SessionLocal()
        self.user_profiles = SQLAlchemyUserProfileRepository(self.session)
        self.training_programs = SQLAlchemyTrainingProgramRepository(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    async def rollback(self):
        self.session.rollback()

    @staticmethod
    def init_database():
        """Инициализация БД"""
        Base.metadata.create_all(bind=engine)