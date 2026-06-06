from uuid import UUID

from app.domain.exceptions.base import EntityNotFoundException
from app.domain.interfaces.repositories.screen import IScreenRepository


class DeleteScreenUseCase:
    def __init__(self, screen_repository: IScreenRepository):
        self.screen_repo = screen_repository

    async def execute(self, screen_id: UUID) -> None:
        success = await self.screen_repo.delete(screen_id)

        if not success:
            raise EntityNotFoundException(
                entity_name="Screen", identifier=str(screen_id)
            )
