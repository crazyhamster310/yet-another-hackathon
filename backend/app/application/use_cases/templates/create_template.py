from app.application.dtos.screen import TemplateCreateDTO, TemplateDTO
from app.domain.entities.screen import Template
from app.domain.interfaces.repositories.template import ITemplateRepository


class CreateTemplateUseCase:
    def __init__(self, template_repository: ITemplateRepository):
        self.template_repo = template_repository

    async def execute(self, dto: TemplateCreateDTO) -> TemplateDTO:
        template_entity = Template(
            name=dto.name,
            widget_type=dto.widget_type,
            title=dto.title,
            content=dto.content,
        )

        saved_template = await self.template_repo.save(template_entity)

        return TemplateDTO.model_validate(saved_template)
