import aiohttp
import json
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

    # async def generate_response(self, messages: list) -> str:
    #     try:
    #         chat_completion = await self.client.chat.completions.create(
    #             model=self.model_name,
    #             messages=messages
    #         )
    #         return chat_completion.choices[0].message.content
    #     except Exception as e:
    #         raise LLMError(f"Ошибка при запросе к DeepSeek API: {e}")

    async def generate_training_program(self, user_data: Dict) -> str:
        """Генерация программы тренировок через LLM"""

        prompt = self._create_prompt(user_data)

        messages = [
                {
                    "role": "system",
                    "content": """Ты профессиональный тренер и спортивный диетолог. 
                    Создавай подробные, персонализированные программы тренировок 
                    на основе предоставленных данных. Отвечай строго в структурированном формате."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        try:
            # async with aiohttp.ClientSession() as session:
            #     async with session.post(
            #             self.api_url,
            #             json=payload,
            #             headers=headers,
            #             timeout=30
            #     ) as response:
            #         if response.status == 200:
            #             result = await response.json()
            #             return result['choices'][0]['message']['content']
            #         else:
            #             error_text = await response.text()
            #             raise LLMServiceError(
            #                 f"API error {response.status}: {error_text}"
            #             )
            chat_completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return chat_completion.choices[0].message.content
        except aiohttp.ClientError as e:
            raise LLMServiceError(f"Network error: {str(e)}")

    def _create_prompt(self, user_data: Dict) -> str:
        """Создание промпта для LLM"""

        prompt = f"""Создай подробную программу тренировок на основе следующих данных:

1. О пользователе:
   - Пол: {user_data.get('gender')}
   - Возраст: {user_data.get('age')} лет
   - Рост: {user_data.get('height')} см
   - Вес: {user_data.get('weight')} кг

2. Цель:
   - Основная цель: {user_data.get('goal')}
   - Дополнительное описание: {user_data.get('custom_goal', 'не указано')}
   - Срок: {user_data.get('months')} месяцев

3. Текущие результаты и опыт:
   - Лучшие результаты: {user_data.get('current_results')}
   - Когда тренировался последний раз: {user_data.get('last_trained')}

4. Расписание тренировок:
   - Тренировок в неделю: {user_data.get('workouts_per_week')}
   - Длительность тренировки: {user_data.get('workout_duration')} минут
   - Предпочитаемый стиль: {user_data.get('training_style')}

5. Ограничения и предпочтения:
   - Ограничения по здоровью: {user_data.get('health_restrictions')}
   - Приоритеты и предпочтения: {user_data.get('preferences')}

Создай программу, которая включает:
1. Общий план на весь период
2. Еженедельное расписание тренировок
3. Конкретные упражнения с подходами и повторениями
4. Рекомендации по прогрессии нагрузок
5. Советы по восстановлению
6. Обрати внимание на ограничения по здоровью

Отформатируй ответ в структурированном виде с разделами и подразделами."""

        return prompt