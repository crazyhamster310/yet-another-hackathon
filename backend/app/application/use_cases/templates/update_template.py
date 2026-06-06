from uuid import UUID

from app.application.dtos.screen import TemplateDTO, TemplateUpdateDTO
from app.domain.exceptions.base import EntityNotFoundException
from app.domain.interfaces.repositories.template import ITemplateRepository


class UpdateTemplateUseCase:
    def __init__(self, template_repository: ITemplateRepository):
        self.template_repo = template_repository

    async def execute(
        self, template_id: UUID, dto: TemplateUpdateDTO
    ) -> TemplateDTO:
        template = await self.template_repo.get_by_id(template_id)
        if not template:
            raise EntityNotFoundException(
                entity_name="Template", entity_id=str(template_id)
            )

        update_data = dto.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(template, field, value)

        updated_template = await self.template_repo.save(template)

        return TemplateDTO.model_validate(updated_template)
