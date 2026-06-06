from typing import Any

from app.domain.exceptions.base import ExternalProviderError
from app.domain.interfaces.providers.ujin import IUjinProvider


class GetUjinNewsUseCase:
    def __init__(self, ujin_provider: IUjinProvider):
        self.ujin_provider = ujin_provider

    async def execute(
        self,
        complex_ids: list[int] | None = None,
        building_ids: list[int] | None = None,
        news_type: str | None = None,
    ) -> list[dict[str, Any]]:
        result = await self.ujin_provider.get_news(
            complexes=complex_ids, buildings=building_ids, type_=news_type
        )

        news_data = result.get("news", {}).get("all", {})
        if news_data["error"]:
            raise ExternalProviderError(
                provider_name="Ujin News",
                detail=f"{news_data['error']}: {news_data.get('details', '')}",
            )

        items = news_data.get("data", {}).get("items", [])

        return items
