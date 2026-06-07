from uuid import UUID

from app.application.dtos.screen import TemplateDTO
from app.domain.exceptions.base import EntityNotFoundException
from app.domain.interfaces.repositories.template import ITemplateRepository


class GetTemplateUseCase:
    def __init__(self, template_repository: ITemplateRepository):
        self.template_repo = template_repository

    async def execute(self, template_id: UUID) -> TemplateDTO:
        template = await self.template_repo.get_by_id(template_id)

        if not template:
            raise EntityNotFoundException(
                entity_name="Template", entity_id=str(template_id)
            )

        return TemplateDTO.model_validate(template)
