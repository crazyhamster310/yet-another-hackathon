from typing import Any

from app.domain.exceptions.base import ExternalProviderError
from app.domain.interfaces.providers.ujin import IUjinProvider


class GetUjinParkingStatsUseCase:
    def __init__(self, ujin_provider: IUjinProvider):
        self.ujin_provider = ujin_provider

    async def execute(
        self,
        complex_ids: list[int] | None = None,
        building_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        result = await self.ujin_provider.get_parking(
            complexes=complex_ids, buildings=building_ids
        )

        parking = result.get("parking", {})

        if "free" in parking and parking["free"]["error"]:
            raise ExternalProviderError(
                provider_name="Ujin Parking",
                detail=parking["free"].get("details", "Request failed"),
            )

        list_spots = parking.get("list", {}).get("data", {}).get("items", [])
        free_spots = parking.get("free", {}).get("data", {}).get("items", [])

        return {
            "free_count": len(free_spots),
            "total_available": len(list_spots),
        }
