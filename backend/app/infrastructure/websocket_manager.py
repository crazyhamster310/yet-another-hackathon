from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, screen_id: UUID, websocket: WebSocket):
        await websocket.accept()
        if screen_id not in self.active_connections:
            self.active_connections[screen_id] = []
        self.active_connections[screen_id].append(websocket)

    def disconnect(self, screen_id: UUID, websocket: WebSocket):
        if screen_id in self.active_connections:
            self.active_connections[screen_id].remove(websocket)
            if not self.active_connections[screen_id]:
                del self.active_connections[screen_id]

    async def send_personal_message(self, message: dict, screen_id: UUID):
        if screen_id in self.active_connections:
            for connection in self.active_connections[screen_id]:
                try:
                    await connection.send_json(message)
                except Exception:  # noqa: S110
                    pass

    async def broadcast_emergency(
        self, screen_ids: list[UUID], is_emergency: bool, text: str = None
    ):
        message = {
            "type": "EMERGENCY_UPDATE",
            "payload": {"is_emergency": is_emergency, "text": text},
        }
        for s_id in screen_ids:
            await self.send_personal_message(message, s_id)


manager = ConnectionManager()
