from fastapi import APIRouter

from app.api.v1.endpoints import data, screens, templates, websockets
from app.core.config import settings

api_router = APIRouter()

api_router.include_router(
    screens.router,
    prefix=f"{settings.API_PREFIX}/v1/screens",
    tags=["Screens"],
)

api_router.include_router(
    templates.router,
    prefix=f"{settings.API_PREFIX}/v1/templates",
    tags=["Templates"],
)

api_router.include_router(
    data.router,
    prefix=f"{settings.API_PREFIX}/v1/data",
    tags=["Ujin Data Proxy"],
)

api_router.include_router(
    websockets.router,
    prefix="/ws",
    tags=["WebSockets"],
)
