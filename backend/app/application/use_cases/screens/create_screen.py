from app.application.dtos.screen import ScreenCreateDTO, ScreenReadDTO
from app.domain.entities.screen import Screen
from app.domain.interfaces.repositories.screen import IScreenRepository


class CreateScreenUseCase:
    def __init__(self, screen_repository: IScreenRepository):
        self.screen_repo = screen_repository

    async def execute(self, dto: ScreenCreateDTO) -> ScreenReadDTO:
        screen_entity = Screen(slug=dto.slug, name=dto.name)

        saved_screen = await self.screen_repo.save(screen_entity)

        return ScreenReadDTO.model_validate(saved_screen)
