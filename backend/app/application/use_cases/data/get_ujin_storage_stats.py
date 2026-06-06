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

        storage = result.get("storage", {})

        if "unassigned" in storage and storage["unassigned"]["error"]:
            print(storage)
            raise ExternalProviderError(
                provider_name="Ujin Storage",
                detail=storage["unassigned"].get("details", "Request failed"),
            )

        list_rooms = storage.get("list", {}).get("data", {}).get("items", [])
        unassigned_rooms = (
            storage.get("unassigned", {}).get("data", {}).get("items", [])
        )

        return {
            "unassigned_count": len(unassigned_rooms),
            "total_available": len(list_rooms),
        }
