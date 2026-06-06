from uuid import UUID

from app.domain.exceptions.base import (
    EntityNotFoundException,
    InvalidSlotIndexError,
)
from app.domain.interfaces.repositories.screen import IScreenRepository
from app.domain.interfaces.repositories.template import ITemplateRepository


class AssignTemplateToSlotUseCase:
    def __init__(
        self,
        screen_repository: IScreenRepository,
        template_repository: ITemplateRepository,
    ):
        self.screen_repo = screen_repository
        self.template_repo = template_repository

    async def execute(
        self, screen_id: UUID, template_id: UUID | None, slot_index: int
    ) -> None:
        if not (0 <= slot_index <= 3):
            raise InvalidSlotIndexError(index=slot_index)

        screen = await self.screen_repo.get_by_id(screen_id)
        if not screen:
            raise EntityNotFoundException(
                entity_name="Screen", entity_id=str(screen_id)
            )

        if template_id:
            template = await self.template_repo.get_by_id(template_id)
            if not template:
                raise EntityNotFoundException(
                    entity_name="Template", entity_id=str(template_id)
                )

        await self.screen_repo.update_slot(
            screen_id=screen_id, slot_index=slot_index, template_id=template_id
        )
