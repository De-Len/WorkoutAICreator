import hashlib
import hmac

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid

from config import config
from src.application.UserProfileUseCases import UserProfileUseCases
from src.application.dto import *
from src.application.exceptions import ApplicationError
from src.infrastructure.llm_client import OpenRouterLLMService
from src.infrastructure.unit_of_work import UnitOfWork

router = APIRouter()
templates = Jinja2Templates(directory="./src/presentation/web/templates")


def get_use_cases():
    """Dependency Injection для use cases"""
    with UnitOfWork() as uow:
        llm_service = OpenRouterLLMService(config)
        use_cases = UserProfileUseCases(
            profile_repository=uow.user_profiles,
            program_repository=uow.training_programs,
            llm_service=llm_service
        )
        yield use_cases


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/api/start_session")
async def start_session(
        request: Request,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    try:
        data = await request.json()
        user_id = data.get('user_id')

        telegram_id = str(user_id) if user_id is not None else None

        # Создаем DTO БЕЗ session_id в DTO, пусть БД сама генерирует
        dto = CreateUserProfileDTO(
            telegram_id=telegram_id
            # session_id убрали - БД сама сгенерирует
        )

        profile = await use_cases.create_profile(dto)

        # Возвращаем ID профиля и session_id (который = id профиля)
        return {
            "profile_id": str(profile.id),  # Используем это как session_id
            "session_id": str(profile.id),  # Для совместимости
            "telegram_id": profile.telegram_id
        }
    except Exception as e:
        print(f"Error in start_session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/step/{step_number}")
async def save_step(
        step_number: int,
        request: Request,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    try:
        data = await request.json()

        # Используем profile_id вместо session_id
        profile_id = data.get('profile_id') or data.get('session_id')

        if not profile_id:
            raise HTTPException(status_code=400, detail="profile_id is required")

        print(f"Saving step {step_number} for profile {profile_id}")

        # Ищем по ID профиля
        profile = await use_cases.profile_repository.get_by_id(uuid.UUID(profile_id))

        if not profile:
            print(f"Profile not found for id: {profile_id}")
            raise HTTPException(status_code=404, detail=f"Profile not found")

        print(f"Found profile: {profile.id}")

        # Обновляем профиль
        if step_number == 1:
            gender = str(data.get('gender', ''))
            age = int(data.get('age', 0)) if data.get('age') not in [None, ''] else 0
            height = int(data.get('height', 0)) if data.get('height') not in [None, ''] else 0
            weight = int(data.get('weight', 0)) if data.get('weight') not in [None, ''] else 0

            profile.gender = gender
            profile.age = age
            profile.height = height
            profile.weight = weight

        elif step_number == 2:
            goal = str(data.get('goal', ''))
            custom_goal = str(data.get('custom_goal', '')) if data.get('goal') == 'custom' else ''
            months = int(data.get('months', 3)) if data.get('months') not in [None, ''] else 3

            profile.goal = goal
            profile.custom_goal = custom_goal
            profile.months = months

        elif step_number == 3:
            current_results = str(data.get('current_results', ''))
            last_trained = str(data.get('last_trained', ''))

            profile.current_results = current_results
            profile.last_trained = last_trained

        elif step_number == 4:
            workouts_per_week = int(data.get('workouts_per_week', 0)) if data.get('workouts_per_week') not in [None,
                                                                                                               ''] else 0
            workout_duration = int(data.get('workout_duration', 0)) if data.get('workout_duration') not in [None,
                                                                                                            ''] else 0
            training_style = str(data.get('training_style', ''))

            profile.workouts_per_week = workouts_per_week
            profile.workout_duration = workout_duration
            profile.training_style = training_style

        elif step_number == 5:
            health_restrictions = str(data.get('health_restrictions', ''))
            preferences = str(data.get('preferences', ''))

            profile.health_restrictions = health_restrictions
            profile.preferences = preferences

        else:
            raise HTTPException(status_code=400, detail=f"Invalid step number: {step_number}")

        # Сохраняем
        updated_profile = await use_cases.profile_repository.update(profile)

        return {
            "status": "success",
            "is_complete": updated_profile.is_complete(),
            "step": step_number,
            "profile_id": str(updated_profile.id)
        }

    except Exception as e:
        print(f"Error in save_step: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/generate_program")
async def generate_program(
        request: Request,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    """Генерация программы тренировок"""
    try:
        data = await request.json()
        session_id = data.get('session_id')

        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")

        request_dto = GenerateProgramRequestDTO(session_id=session_id)
        program = await use_cases.generate_program(request_dto)

        return {
            "status": "success",
            "program_id": str(program.id),
            "content": program.content
        }
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in generate_program: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/program/{session_id}")
async def get_program(
        session_id: str,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    """Получение программы тренировок"""
    try:
        programs = await use_cases.get_profile_programs(session_id)
        if not programs:
            raise HTTPException(status_code=404, detail="Program not found")

        latest_program = max(programs, key=lambda p: p.created_at)

        # Преобразуем в словарь для JSON
        return {
            "id": str(latest_program.id),
            "user_profile_id": str(latest_program.user_profile_id),
            "content": latest_program.content,
            "created_at": latest_program.created_at.isoformat()
        }
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in get_program: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def validate_telegram_data(data: str, token: str) -> bool:
    """Проверяет подпись данных от Telegram"""
    try:
        # Извлекаем хэш из данных
        data_dict = dict(param.split('=') for param in data.split('&'))
        received_hash = data_dict.pop('hash', '')

        # Сортируем и формируем строку для проверки
        data_check_string = '\n'.join(
            f'{k}={v}' for k, v in sorted(data_dict.items())
        )

        # Вычисляем секретный ключ
        secret_key = hmac.new(
            b"WebAppData",
            token.encode(),
            hashlib.sha256
        ).digest()

        # Вычисляем хэш
        computed_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        return computed_hash == received_hash
    except:
        return False