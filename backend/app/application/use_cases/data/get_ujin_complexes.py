from typing import Any

from app.domain.exceptions.base import ExternalProviderError
from app.domain.interfaces.providers.ujin import IUjinProvider


class GetUjinComplexesUseCase:
    def __init__(self, ujin_provider: IUjinProvider):
        self.ujin_provider = ujin_provider

    async def execute(self) -> dict[str, Any]:
        result = await self.ujin_provider.get_complexes()

        complexes_data = result.get("complexes", {})
        if complexes_data.get("error"):
            raise ExternalProviderError(
                provider_name="Ujin Complexes",
                detail=complexes_data.get("details", "Request failed"),
            )

        return complexes_data