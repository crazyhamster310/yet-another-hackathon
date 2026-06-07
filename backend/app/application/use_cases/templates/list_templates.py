from app.application.dtos.screen import TemplateDTO
from app.domain.interfaces.repositories.template import ITemplateRepository


class ListTemplatesUseCase:
    def __init__(self, template_repository: ITemplateRepository):
        self.template_repo = template_repository

    async def execute(self) -> list[TemplateDTO]:
        templates = await self.template_repo.list_all()

        return [TemplateDTO.model_validate(t) for t in templates]
