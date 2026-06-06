from typing import Any

from app.domain.exceptions.base import ExternalProviderError
from app.domain.interfaces.providers.ujin import IUjinProvider


class GetUjinBuildingsUseCase:
    def __init__(self, ujin_provider: IUjinProvider):
        self.ujin_provider = ujin_provider

    async def execute(
        self, complex_ids: list[int] | None = None
    ) -> dict[str, Any]:
        result = await self.ujin_provider.get_buildings(complexes=complex_ids)

        buildings_data = result.get("buildings", {})
        if buildings_data.get("error"):
            raise ExternalProviderError(
                provider_name="Ujin Buildings",
                detail=buildings_data.get("details", "Request failed"),
            )

        return buildings_data