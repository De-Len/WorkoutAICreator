from abc import abstractmethod, ABC
from typing import Optional
from uuid import UUID


class UserProfileRepository(ABC):
    """Абстрактный репозиторий для профилей пользователей"""

    @abstractmethod
    async def get_by_id(self, profile_id: UUID) -> Optional[UserProfile]:
        pass

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: str) -> Optional[UserProfile]:
        pass

    @abstractmethod
    async def get_by_session_id(self, session_id: str) -> Optional[UserProfile]:
        pass

    @abstractmethod
    async def save(self, profile: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    async def update(self, profile: UserProfile) -> UserProfile:
        pass