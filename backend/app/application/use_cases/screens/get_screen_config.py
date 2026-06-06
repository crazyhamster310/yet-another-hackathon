from app.application.dtos.screen import ScreenReadDTO
from app.domain.exceptions.base import EntityNotFoundException
from app.domain.interfaces.repositories.screen import IScreenRepository


class GetScreenConfigUseCase:
    def __init__(self, screen_repository: IScreenRepository):
        self.screen_repo = screen_repository

    async def execute(self, slug: str) -> ScreenReadDTO:
        screen = await self.screen_repo.get_by_slug(slug)

        if not screen:
            raise EntityNotFoundException(
                entity_name="Screen", entity_id=slug
            )

        return ScreenReadDTO.model_validate(screen)
