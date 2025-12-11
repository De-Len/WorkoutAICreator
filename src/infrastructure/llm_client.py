import aiohttp
from typing import Dict

from openai import AsyncOpenAI

from config import Config
from src.application.exceptions import LLMServiceError
from src.core.interfaces.LLMService import LLMService


class OpenRouterLLMService(LLMService):
    """Реализация LLM сервиса через OpenRouter API"""

    def __init__(self, config: Config):
        self.model_name = config.llm.model_name
        self.client = AsyncOpenAI(
            api_key=config.llm.api_key,
            base_url=config.llm.api_url,
        )

    async def generate_training_program(self, user_data: Dict) -> str:
        """Генерация программы тренировок через LLM"""

        prompt = self._create_prompt(user_data)

        messages = [
                {
                    "role": "system",
                    "content": """Ты профессиональный тренер и спортивный диетолог. 
                    Создавай подробные, персонализированные программы тренировок 
                    на основе предоставленных данных. Отвечай строго в структурированном формате. Не пиши таблицы!"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        try:
            chat_completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return chat_completion.choices[0].message.content
        except aiohttp.ClientError as e:
            raise LLMServiceError(f"Network error: {str(e)}")

    def _create_prompt(self, user_data: Dict) -> str:
        """Создание компактного промпта для LLM"""

        # Создайте более компактный запрос
        return f"""Создай программу тренировок для:
Пол: {user_data.get('gender')}, Возраст: {user_data.get('age')}
Цель: {user_data.get('goal')} за {user_data.get('months')} месяцев
Опыт: {user_data.get('last_trained')}
Тренировок/неделю: {user_data.get('workouts_per_week')} по {user_data.get('workout_duration')} мин
Стиль: {user_data.get('training_style')}
Ограничения: {user_data.get('health_restrictions') or 'нет'}
Предпочтения: {user_data.get('preferences') or 'стандартные'}

Создай структурированную программу с:
1. Еженедельным планом
2. Упражнениями и подходами
3. Прогрессией нагрузок
4. Рекомендациями
"""
