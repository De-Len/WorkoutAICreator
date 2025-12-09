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
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        "🏋️ Добро пожаловать в генератор программ тренировок!\n\n"
        "Я помогу создать персонализированную программу тренировок "
        "на основе ваших целей и возможностей.\n\n"
        "Используйте команды:\n"
        "/form - начать заполнение формы\n"
        "/web - открыть веб-интерфейс\n"
        "/cancel - отменить текущее заполнение"
    )


@router.message(Command("web"))
async def cmd_web(message: types.Message):
    web_app_url = "https://manually-effective-dipper.cloudpub.ru"

    # Используй обычную ссылку вместо Web App
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📱 Открыть веб-форму",
            url=web_app_url  # Просто URL, не WebApp
        )]
    ])

    await message.answer(
        "Откройте веб-форму для создания программы тренировок:",
        reply_markup=keyboard
    )


@router.message(Command("form"))
async def cmd_form(message: types.Message, state: FSMContext):
    # Начинаем новую сессию
    session_id = str(uuid.uuid4())
    await state.update_data(session_id=session_id)

    # Создаем профиль в БД
    use_cases = get_use_cases()
    dto = CreateUserProfileDTO(
        telegram_id=str(message.from_user.id),
        session_id=session_id
    )

    try:
        await use_cases.create_profile(dto)

        # Начинаем заполнение формы
        await message.answer(
            "Шаг 1 из 5: Расскажите о себе\n\n"
            "Выберите ваш пол:",
            reply_markup=get_gender_keyboard()
        )
        await state.set_state(UserProfileStates.waiting_gender)
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


@router.callback_query(F.data.startswith("gender_"))
async def process_gender(callback: types.CallbackQuery, state: FSMContext):
    gender_value = callback.data.split("_")[1]

    # Сохраняем в состоянии
    await state.update_data(gender=gender_value)

    await callback.message.edit_text("✅ Пол сохранен")
    await callback.message.answer(
        "Шаг 1 из 5: Расскажите о себе\n\n"
        "Введите ваш возраст (лет):"
    )
    await state.set_state(UserProfileStates.waiting_age)


@router.message(UserProfileStates.waiting_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 10 or age > 100:
            await message.answer("Пожалуйста, введите возраст от 10 до 100 лет:")
            return

        # Сохраняем шаг в БД
        state_data = await state.get_data()
        use_cases = get_use_cases()

        dto = UserProfileStep1DTO(
            gender=state_data['gender'],
            age=age,
            height=0,  # временные значения
            weight=0
        )

        await use_cases.update_step1(state_data['session_id'], dto)

        await message.answer("✅ Возраст сохранен")
        await message.answer("Введите ваш рост (в см):")
        await state.set_state(UserProfileStates.waiting_height)
    except ValueError:
        await message.answer("Пожалуйста, введите число:")


# Аналогичные обработчики для остальных шагов...

@router.message(Command("cancel"))
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Заполнение формы отменено.")