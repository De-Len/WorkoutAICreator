from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from config import config
import uuid

from src.application.UserProfileUseCases import UserProfileUseCases
from src.application.dto import CreateUserProfileDTO, UserProfileStep1DTO
from src.infrastructure.llm_client import OpenRouterLLMService
from src.infrastructure.unit_of_work import UnitOfWork
from src.presentation.telegram_bot.keyboards import get_gender_keyboard
from src.presentation.telegram_bot.states import UserProfileStates

router = Router()


def get_use_cases():
    """Получение use cases для обработчиков"""
    with UnitOfWork() as uow:
        llm_service = OpenRouterLLMService(config)
        return UserProfileUseCases(
            profile_repository=uow.user_profiles,
            program_repository=uow.training_programs,
            llm_service=llm_service
        )


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # URL для Mini App - твой облачный адрес
    web_app_url = config.web.external_url

    user = message.from_user
    user_tag = f"@{user.username}" if user.username else f"id{user.id}"
    print(f"👤 {user_tag} запустил бота")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏋️ Открыть приложение",
                web_app=WebAppInfo(url=web_app_url)
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ Помощь",
                callback_data="help"
            )
        ]
    ])

    await message.answer(
        "🏋️ Добро пожаловать в генератор тренировок!\n\n"
        "Нажмите кнопку ниже, чтобы открыть приложение:",
        reply_markup=keyboard
    )


@router.callback_query(F.data == "help")
async def show_help(callback: types.CallbackQuery):
    await callback.message.answer(
        "📱 Это мини-приложение в Telegram позволяет:\n"
        "1. Создать персонализированную программу тренировок\n"
        "2. Сохранить ваши данные\n"
        "3. Получить рекомендации от ИИ\n\n"
        "Просто нажмите кнопку 'Открыть приложение'!"
    )
