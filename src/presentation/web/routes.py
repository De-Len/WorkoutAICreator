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
async def start_session(use_cases: UserProfileUseCases = Depends(get_use_cases)):
    """Начало новой сессии"""
    session_id = str(uuid.uuid4())

    dto = CreateUserProfileDTO(
        session_id=session_id
    )

    try:
        profile = await use_cases.create_profile(dto)
        return {"session_id": session_id, "profile_id": str(profile.id)}
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/step/1")
async def save_step1(
        dto: UserProfileStep1DTO,
        session_id: str,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    """Сохранение шага 1"""
    try:
        profile = await use_cases.update_step1(session_id, dto)
        return {"status": "success", "is_complete": profile.is_complete}
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/api/step/2")
async def save_step2(
        dto: UserProfileStep2DTO,
        session_id: str,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    """Сохранение шага 2"""
    try:
        profile = await use_cases.update_step2(session_id, dto)
        return {"status": "success", "is_complete": profile.is_complete}
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Аналогично для шагов 3, 4, 5

@router.post("/api/generate_program")
async def generate_program(
        request: GenerateProgramRequestDTO,
        use_cases: UserProfileUseCases = Depends(get_use_cases)
):
    """Генерация программы тренировок"""
    try:
        program = await use_cases.generate_program(request)
        return {
            "status": "success",
            "program_id": str(program.id),
            "content": program.content
        }
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
        return latest_program
    except ApplicationError as e:
        raise HTTPException(status_code=400, detail=str(e))