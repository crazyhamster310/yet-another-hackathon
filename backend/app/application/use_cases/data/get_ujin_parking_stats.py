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

        parking = result["parking"]

        if parking["list"]["error"]:
            raise ExternalProviderError(
                provider_name="Ujin Parking",
                detail=parking["list"].get("details", "Request failed"),
            )

        parking_list_data = parking["list"]

        total_count = 0
        unassigned_count = 0

        complexes = parking_list_data["data"]["items"]
        for complex_item in complexes:
            buildings = complex_item["buildings"]
            for building in buildings:
                zones = building["zones"]
                for zone in zones:
                    spots = zone["spots"]
                    for spot in spots:
                        total_count += 1
                        if spot["assignment_type"] == "unassigned":
                            unassigned_count += 1

        return {
            "total_count": total_count,
            "unassigned_count": unassigned_count,
        }
