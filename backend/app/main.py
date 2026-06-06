from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import (
    configuration_exception_handler,
    domain_exception_handler,
    entity_not_found_exception_handler,
    external_provider_exception_handler,
)
from app.api.v1.api import api_router
from app.core.config import settings
from app.domain.exceptions.base import (
    ConfigurationError,
    DomainException,
    EntityNotFoundException,
    ExternalProviderError,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        version="1.0.0",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(DomainException, domain_exception_handler)
    app.add_exception_handler(
        EntityNotFoundException, entity_not_found_exception_handler
    )
    app.add_exception_handler(
        ExternalProviderError, external_provider_exception_handler
    )
    app.add_exception_handler(
        ConfigurationError, configuration_exception_handler
    )

    app.include_router(api_router)

    @app.get("/ping", tags=["Health"])
    async def health_check():
        return {"status": "ok", "app": settings.APP_NAME}

    return app


app = create_app()
