from uuid import UUID

from app.domain.exceptions.base import EntityNotFoundException
from app.domain.interfaces.repositories.template import ITemplateRepository


class DeleteTemplateUseCase:
    def __init__(self, template_repository: ITemplateRepository):
        self.template_repo = template_repository

    async def execute(self, template_id: UUID) -> None:
        success = await self.template_repo.delete(template_id)

        if not success:
            raise EntityNotFoundException(
                entity_name="Template", entity_id=str(template_id)
            )
