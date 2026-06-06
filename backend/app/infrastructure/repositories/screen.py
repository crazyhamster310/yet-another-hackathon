from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.screen import Screen as ScreenEntity
from app.domain.entities.screen import Template as TemplateEntity
from app.domain.interfaces.repositories.screen import IScreenRepository
from app.infrastructure.database.models import ScreenModel, ScreenSlotModel
from app.infrastructure.repositories.base import BaseRepository


class SqlAlchemyScreenRepository(
    BaseRepository[ScreenModel], IScreenRepository
):
    def __init__(self, session: AsyncSession):
        super().__init__(ScreenModel, session)

    def _to_entity(self, model: ScreenModel) -> ScreenEntity:
        layout = {i: None for i in range(4)}
        for slot in model.slots:
            if slot.template:
                layout[slot.slot_index] = TemplateEntity.model_validate(
                    slot.template
                )

        return ScreenEntity(
            id=model.id,
            slug=model.slug,
            name=model.name,
            is_emergency=model.is_emergency,
            emergency_text=model.emergency_text,
            layout=layout,
        )

    async def get_by_id(self, screen_id: UUID) -> ScreenEntity | None:
        query = (
            select(ScreenModel)
            .where(ScreenModel.id == screen_id)
            .options(
                selectinload(ScreenModel.slots).selectinload(
                    ScreenSlotModel.template
                )
            )
        )
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_slug(self, slug: str) -> ScreenEntity | None:
        query = (
            select(ScreenModel)
            .where(ScreenModel.slug == slug)
            .options(
                selectinload(ScreenModel.slots).selectinload(
                    ScreenSlotModel.template
                )
            )
        )
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_all(self) -> list[ScreenEntity]:
        query = select(ScreenModel).options(
            selectinload(ScreenModel.slots).selectinload(
                ScreenSlotModel.template
            )
        )
        result = await self.session.execute(query)
        return [self._to_entity(m) for m in result.scalars().all()]

    async def save(self, screen: ScreenEntity) -> ScreenEntity:
        query = select(ScreenModel).where(ScreenModel.id == screen.id)
        res = await self.session.execute(query)
        model = res.scalar_one_or_none()

        if not model:
            model = ScreenModel(
                id=screen.id, slug=screen.slug, name=screen.name
            )
            self.session.add(model)

        model.is_emergency = screen.is_emergency
        model.emergency_text = screen.emergency_text

        existing_slots = {
            slot.slot_index: slot for slot in (model.slots or [])
        }

        for i in range(4):
            template_id = screen.layout[i].id if screen.layout[i] else None

            if i in existing_slots:
                existing_slots[i].template_id = template_id
            else:
                new_slot = ScreenSlotModel(
                    screen_id=model.id, slot_index=i, template_id=template_id
                )
                self.session.add(new_slot)

        await self.session.flush()
        return await self.get_by_id(model.id)

    async def update_emergency_status(
        self,
        screen_ids: list[UUID],
        is_emergency: bool,
        text: str | None = None,
    ) -> None:
        query = (
            update(ScreenModel)
            .where(ScreenModel.id.in_(screen_ids))
            .values(is_emergency=is_emergency, emergency_text=text)
        )
        await self.session.execute(query)

    async def update_slot(
        self, screen_id: UUID, slot_index: int, template_id: UUID | None
    ) -> None:
        query = select(ScreenSlotModel).where(
            ScreenSlotModel.screen_id == screen_id,
            ScreenSlotModel.slot_index == slot_index,
        )
        result = await self.session.execute(query)
        slot = result.scalar_one_or_none()

        if slot:
            slot.template_id = template_id
        else:
            new_slot = ScreenSlotModel(
                screen_id=screen_id,
                slot_index=slot_index,
                template_id=template_id,
            )
            self.session.add(new_slot)

        await self.session.flush()
