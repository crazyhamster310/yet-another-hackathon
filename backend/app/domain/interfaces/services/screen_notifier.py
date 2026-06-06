from abc import ABC, abstractmethod
from uuid import UUID


class IScreenNotifier(ABC):
    @abstractmethod
    async def notify_emergency_update(
        self,
        screen_ids: list[UUID],
        is_emergency: bool,
        text: str | None = None,
    ) -> None:
        pass
