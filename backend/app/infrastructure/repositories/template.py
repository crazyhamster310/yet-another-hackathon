from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.screen import Template as TemplateEntity
from app.domain.interfaces.repositories.template import ITemplateRepository
from app.infrastructure.database.models import TemplateModel
from app.infrastructure.repositories.base import BaseRepository


class SqlAlchemyTemplateRepository(
    BaseRepository[TemplateModel], ITemplateRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(TemplateModel, session)

    def _to_entity(self, model: TemplateModel) -> TemplateEntity:
        return TemplateEntity.model_validate(model)

    async def get_by_id(self, template_id: UUID) -> TemplateEntity | None:
        model = await self.get(template_id)
        return self._to_entity(model) if model else None

    async def list_all(self) -> list[TemplateEntity]:
        models = await self.get_multi()
        return [self._to_entity(m) for m in models]

    async def save(self, template: TemplateEntity) -> TemplateEntity:
        query = select(TemplateModel).where(TemplateModel.id == template.id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        data = {
            "name": template.name,
            "widget_type": template.widget_type,
            "settings": template.settings,
            "content_rotation_settings": template.content_rotation_settings,
        }

        if model:
            model = await self.update(db_obj=model, obj_in_data=data)
        else:
            data["id"] = template.id
            model = await self.create(obj_in_data=data)

        return self._to_entity(model)

    async def delete(self, template_id: UUID) -> bool:
        return await super().delete(id=template_id)
