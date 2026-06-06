from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.screen import Screen


class IScreenRepository(ABC):
    @abstractmethod
    async def get_by_id(self, screen_id: UUID) -> Screen | None:
        pass

    @abstractmethod
    async def get_by_slug(self, slug: str) -> Screen | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Screen]:
        pass

    @abstractmethod
    async def save(self, screen: Screen) -> Screen:
        pass

    @abstractmethod
    async def update_emergency_status(
        self,
        screen_ids: list[UUID],
        is_emergency: bool,
        text: str | None = None,
    ) -> None:
        pass

    @abstractmethod
    async def update_slot(
        self, screen_id: UUID, slot_index: int, template_id: UUID | None
    ) -> None:
        pass

    @abstractmethod
    async def delete(self, screen_id: UUID) -> bool:
        pass
