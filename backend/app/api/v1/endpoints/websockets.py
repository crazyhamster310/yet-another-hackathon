import logging
from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.infrastructure.websocket_manager import manager

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/{screen_id}")
async def websocket_endpoint(websocket: WebSocket, screen_id: UUID):
    await manager.connect(screen_id, websocket)
    logger.info(f"Client connected to WebSocket: Screen ID {screen_id}")

    try:
        while True:
            data = await websocket.receive_text()

            if data == "ping":
                await websocket.send_text("pong")

    except WebSocketDisconnect:
        manager.disconnect(screen_id, websocket)
        logger.info(f"Client disconnected: Screen ID {screen_id}")
    except Exception as e:
        manager.disconnect(screen_id, websocket)
        logger.error(f"WebSocket error for Screen {screen_id}: {str(e)}")
