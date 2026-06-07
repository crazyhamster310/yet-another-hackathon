from uuid import UUID

from app.domain.interfaces.services.screen_notifier import IScreenNotifier
from app.infrastructure.websocket_manager import manager


class WebSocketScreenNotifier(IScreenNotifier):
    async def notify_emergency_update(
        self,
        screen_ids: list[UUID],
        is_emergency: bool,
        text: str | None = None,
    ) -> None:
        await manager.broadcast_emergency(
            screen_ids=screen_ids, is_emergency=is_emergency, text=text or ""
        )
