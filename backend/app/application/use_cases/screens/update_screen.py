from uuid import UUID

from app.application.dtos.screen import ScreenReadDTO, ScreenUpdateDTO
from app.domain.exceptions.base import (
    ConfigurationError,
    EntityNotFoundException,
)
from app.domain.interfaces.providers.ujin import IUjinProvider
from app.domain.interfaces.repositories.screen import IScreenRepository


class UpdateScreenUseCase:
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

    async def execute(
        self, screen_id: UUID, dto: ScreenUpdateDTO
    ) -> ScreenReadDTO:
        screen = await self.screen_repo.get_by_id(screen_id)
        if not screen:
            raise EntityNotFoundException(
                entity_name="Screen", identifier=str(screen_id)
            )

        new_complex_id = (
            dto.complex_id if dto.complex_id is not None else screen.complex_id
        )
        new_building_id = (
            dto.building_id
            if dto.building_id is not None
            else screen.building_id
        )

        if dto.complex_id is not None or dto.building_id is not None:
            if new_building_id and not new_complex_id:
                raise ConfigurationError(
                    "Нельзя оставить здание без привязки к ЖК."
                )
            await self._validate_ujin_objects(new_complex_id, new_building_id)

        update_data = dto.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(screen, field, value)

        updated_screen = await self.screen_repo.save(screen)

        return ScreenReadDTO.model_validate(updated_screen)
