from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions.base import (
    ConfigurationError,
    DomainException,
    EntityNotFoundException,
    ExternalProviderError,
)


async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "type": "domain_error"},
    )


async def entity_not_found_exception_handler(
    request: Request, exc: EntityNotFoundException
):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message, "type": "not_found"},
    )


async def external_provider_exception_handler(
    request: Request, exc: ExternalProviderError
):
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content={"detail": exc.message, "type": "external_api_error"},
    )


async def configuration_exception_handler(
    request: Request, exc: ConfigurationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.message, "type": "configuration_error"},
    )
