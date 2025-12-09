from abc import ABC, abstractmethod
from typing import Dict

class LLMService(ABC):
    @abstractmethod
    async def generate_training_program(self, user_data: Dict) -> str:
        pass