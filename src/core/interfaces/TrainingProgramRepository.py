from abc import abstractmethod, ABC


class TrainingProgramRepository(ABC):
    """Абстрактный репозиторий для программ тренировок"""

    @abstractmethod
    async def save(self, program: TrainingProgram) -> TrainingProgram:
        pass

    @abstractmethod
    async def get_by_user_profile(self, profile_id: UUID) -> List[TrainingProgram]:
        pass