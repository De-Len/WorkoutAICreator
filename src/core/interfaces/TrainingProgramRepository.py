from abc import abstractmethod, ABC
from uuid import UUID

from src.core.entities.TrainingProgram import TrainingProgram


class TrainingProgramRepository(ABC):
    @abstractmethod
    async def save(self, program: TrainingProgram) -> TrainingProgram:
        pass

    @abstractmethod
    async def get_by_user_profile(self, profile_id: UUID) -> list[TrainingProgram]:
        pass