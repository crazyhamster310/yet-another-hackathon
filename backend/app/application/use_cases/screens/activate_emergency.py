from uuid import UUID

from app.application.dtos.screen import EmergencyUpdateDTO
from app.domain.interfaces.repositories.screen import IScreenRepository


class ActivateEmergencyUseCase:
    def __init__(self, screen_repository: IScreenRepository):
        self.screen_repo = screen_repository

    async def execute(self, dto: EmergencyUpdateDTO) -> None:
        target_ids: list[UUID] = []

        if dto.screen_ids:
            target_ids = dto.screen_ids
        else:
            all_screens = await self.screen_repo.list_all()
            target_ids = [screen.id for screen in all_screens]

        if not target_ids:
            return

        await self.screen_repo.update_emergency_status(
            screen_ids=target_ids,
            is_emergency=dto.is_emergency,
            text=dto.emergency_text,
        )

        # Мб, потом будут вебсокеты
