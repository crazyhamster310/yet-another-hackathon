from app.application.dtos.screen import ScreenReadDTO
from app.domain.interfaces.repositories.screen import IScreenRepository


class ListScreensUseCase:
    def __init__(self, screen_repository: IScreenRepository):
        self.screen_repo = screen_repository

    async def execute(self) -> list[ScreenReadDTO]:
        screens = await self.screen_repo.list_all()
        return [ScreenReadDTO.model_validate(s) for s in screens]
