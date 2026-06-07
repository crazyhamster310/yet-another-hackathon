from typing import Any

from app.domain.exceptions.base import ExternalProviderError
from app.domain.interfaces.providers.ujin import IUjinProvider


class GetUjinStorageStatsUseCase:
    def __init__(self, ujin_provider: IUjinProvider):
        self.ujin_provider = ujin_provider

    async def execute(
        self,
        complex_ids: list[int] | None = None,
        building_ids: list[int] | None = None,
    ) -> dict[str, Any]:
        result = await self.ujin_provider.get_storage(
            complexes=complex_ids, buildings=building_ids
        )

        storage = result["storage"]

        if storage["list"]["error"]:
            raise ExternalProviderError(
                provider_name="Ujin Storage",
                detail=storage["list"].get("details", "Request failed"),
            )

        storage_list_data = storage["list"]

        total_count = 0
        unassigned_count = 0

        complexes = storage_list_data["data"]["items"]
        for complex_item in complexes:
            buildings = complex_item["buildings"]
            for building in buildings:
                storages = building["storages"]
                for storage_unit in storages:
                    total_count += 1
                    if storage_unit["assignment_type"] == "unassigned":
                        unassigned_count += 1

        return {
            "total_count": total_count,
            "unassigned_count": unassigned_count,
        }
