from app.application.dtos.screen import ScreenCreateDTO, ScreenReadDTO
from app.domain.entities.screen import Screen
from app.domain.exceptions.base import (
    ConfigurationError,
    EntityAlreadyExistsException,
)
from app.domain.interfaces.providers.ujin import IUjinProvider
from app.domain.interfaces.repositories.screen import IScreenRepository


class CreateScreenUseCase:
    def __init__(
        self,
        screen_repository: IScreenRepository,
        ujin_provider: IUjinProvider,
    ):
        self.screen_repo = screen_repository
        self.ujin_provider = ujin_provider

    async def _validate_ujin_objects(
        self, complex_id: int | None, building_id: int | None
    ):
        if complex_id:
            complexes_resp = await self.ujin_provider.get_complexes()
            items = complexes_resp["complexes"]["data"]["items"]

            if not any(c.get("id") == complex_id for c in items):
                raise ConfigurationError(f"ЖК с ID {complex_id} не найден.")

        if building_id:
            if not complex_id:
                raise ConfigurationError(
                    "Нельзя указать здание без указания ID ЖК."
                )

            buildings_resp = await self.ujin_provider.get_buildings(
                complexes=[complex_id]
            )
            buildings = buildings_resp["buildings"]["data"]["buildings"]

            if not any(b.get("id") == building_id for b in buildings):
                raise ConfigurationError(
                    f"Здание с ID {building_id} не найдено в составе ЖК {complex_id}."
                )

    async def execute(self, dto: ScreenCreateDTO) -> ScreenReadDTO:
        existing_screen = await self.screen_repo.get_by_slug(dto.slug)
        if existing_screen:
            raise EntityAlreadyExistsException(
                entity_name="Screen", entity_id=dto.slug
            )

        await self._validate_ujin_objects(dto.complex_id, dto.building_id)

        screen_entity = Screen(
            slug=dto.slug,
            name=dto.name,
            complex_id=dto.complex_id,
            building_id=dto.building_id,
        )

        saved_screen = await self.screen_repo.save(screen_entity)

        return ScreenReadDTO.model_validate(saved_screen)
