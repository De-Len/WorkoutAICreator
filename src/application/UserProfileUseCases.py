from typing import Optional
from uuid import UUID

from src.application.dto import CreateUserProfileDTO, UserProfileResponseDTO, UserProfileStep2DTO, \
    GenerateProgramRequestDTO, TrainingProgramResponseDTO, UserProfileStep1DTO
from src.application.exceptions import ProfileNotFoundError, IncompleteProfileError
from src.core.entities.TrainingProgram import TrainingProgram
from src.core.entities.UserProfile import UserProfile
from src.core.interfaces.LLMService import LLMService
from src.core.interfaces.TrainingProgramRepository import TrainingProgramRepository
from src.core.interfaces.UserProfileRepository import UserProfileRepository


class UserProfileUseCases:
    """Use Cases для работы с профилями пользователей"""

    def __init__(
            self,
            profile_repository: UserProfileRepository,
            program_repository: TrainingProgramRepository,
            llm_service: LLMService
    ):
        self.profile_repository = profile_repository
        self.program_repository = program_repository
        self.llm_service = llm_service

    async def create_profile(self, dto: CreateUserProfileDTO) -> UserProfileResponseDTO:
        """Создание нового профиля"""
        profile = UserProfile(
            telegram_id=dto.telegram_id
        )
        profile = await self.profile_repository.save(profile)

        return UserProfileResponseDTO(
            id=profile.id,
            telegram_id=profile.telegram_id,
            is_complete=profile.is_complete(),
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

    async def update_step1(
            self,
            session_id: str,
            dto: UserProfileStep1DTO
    ) -> UserProfileResponseDTO:
        """Обновление шага 1 профиля"""
        profile = await self.profile_repository.get_by_session_id(session_id)
        if not profile:
            raise ProfileNotFoundError(session_id)

        profile.update(
            gender=dto.gender,
            age=dto.age,
            height=dto.height,
            weight=dto.weight
        )

        updated_profile = await self.profile_repository.update(profile)

        return UserProfileResponseDTO(
            id=updated_profile.id,
            telegram_id=updated_profile.telegram_id,
            is_complete=updated_profile.is_complete(),
            created_at=updated_profile.created_at,
            updated_at=updated_profile.updated_at
        )

    async def update_step2(
            self,
            session_id: str,
            dto: UserProfileStep2DTO
    ) -> UserProfileResponseDTO:
        """Обновление шага 2 профиля"""
        profile = await self.profile_repository.get_by_session_id(session_id)
        if not profile:
            raise ProfileNotFoundError(session_id)

        profile.update(
            goal=dto.goal,
            custom_goal=dto.custom_goal,
            months=dto.months
        )

        updated_profile = await self.profile_repository.update(profile)

        return UserProfileResponseDTO(
            id=updated_profile.id,
            telegram_id=updated_profile.telegram_id,
            is_complete=updated_profile.is_complete(),
            created_at=updated_profile.created_at,
            updated_at=updated_profile.updated_at
        )

    # Аналогичные методы для шагов 3, 4, 5

    async def generate_program(
            self,
            dto: GenerateProgramRequestDTO
    ) -> TrainingProgramResponseDTO:
        """Генерация программы тренировок"""
        profile = await self.profile_repository.get_by_session_id(dto.session_id)
        if not profile:
            raise ProfileNotFoundError(dto.session_id)

        if not profile.is_complete():
            raise IncompleteProfileError()

        # Подготовка данных для LLM
        user_data = {
            "gender": profile.gender.value,
            "age": profile.age,
            "height": profile.height,
            "weight": profile.weight,
            "goal": profile.goal.value,
            "custom_goal": profile.custom_goal,
            "months": profile.months,
            "current_results": profile.current_results,
            "last_trained": profile.last_trained.value,
            "workouts_per_week": profile.workouts_per_week,
            "workout_duration": profile.workout_duration,
            "training_style": profile.training_style.value,
            "health_restrictions": profile.health_restrictions,
            "preferences": profile.preferences,
        }

        # Генерация программы
        program_content = await self.llm_service.generate_training_program(user_data)

        # Сохранение программы
        program = TrainingProgram(
            user_profile_id=profile.id,
            content=program_content
        )

        saved_program = await self.program_repository.save(program)

        # Обновление профиля
        profile.generated_program = program_content
        await self.profile_repository.update(profile)

        return TrainingProgramResponseDTO(
            id=saved_program.id,
            user_profile_id=saved_program.user_profile_id,
            content=saved_program.content,
            created_at=saved_program.created_at
        )

    async def get_profile_programs(
            self,
            session_id: str
    ) -> list[TrainingProgramResponseDTO]:
        """Получение программ пользователя"""
        profile = await self.profile_repository.get_by_session_id(session_id)
        if not profile:
            raise ProfileNotFoundError(session_id)

        programs = await self.program_repository.get_by_user_profile(profile.id)

        return [
            TrainingProgramResponseDTO(
                id=program.id,
                user_profile_id=program.user_profile_id,
                content=program.content,
                created_at=program.created_at
            )
            for program in programs
        ]