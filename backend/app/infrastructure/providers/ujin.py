import asyncio

import httpx

from app.domain.interfaces.providers.ujin import IUjinProvider


class UjinProvider(IUjinProvider):
    def __init__(
        self,
        token: str,
        base_url: str = "https://hck-api.unicorn.icu",
        per_page: int = 1000,
        timeout: int = 10,
    ):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.per_page = per_page
        self.timeout = httpx.Timeout(float(timeout))

    async def _safe_request(
        self, client: httpx.AsyncClient, endpoint: str, params: dict
    ) -> dict:
        try:
            response = await client.get(
                f"{self.base_url}{endpoint}",
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": f"HTTP {e.response.status_code}",
                "details": e.response.text,
            }
        except Exception as e:
            return {"error": "Request failed", "details": str(e)}

    async def get_complexes(self) -> dict:
        params = {"token": self.token}
        async with httpx.AsyncClient() as client:
            res = await self._safe_request(
                client, "/api/v1/complex/list/", params
            )
            return {"complexes": res}

    async def get_buildings(self, complexes: list[int] | None = None) -> dict:
        params = {"token": self.token, "per_page": self.per_page}
        if complexes:
            params["complexes[]"] = complexes

        async with httpx.AsyncClient() as client:
            res = await self._safe_request(
                client, "/api/v1/buildings/get-list-crm/", params
            )
            return {"buildings": res}

    async def get_parking(
        self,
        complexes: list[int] | None = None,
        buildings: list[int] | None = None,
    ) -> dict:
        params = {"token": self.token}
        if complexes:
            params["complexes[]"] = complexes
        if buildings:
            params["buildings[]"] = buildings

        endpoints = [
            "list",
            "free",
        ]

        async with httpx.AsyncClient() as client:
            tasks = [
                self._safe_request(client, f"/api/v1/parking/{e}", params)
                for e in endpoints
            ]
            results = await asyncio.gather(*tasks)

            return {
                "parking": {
                    endpoints[i]: results[i] for i in range(len(endpoints))
                }
            }

    async def get_storage(
        self,
        complexes: list[int] | None = None,
        buildings: list[int] | None = None,
    ) -> dict:
        params = {"token": self.token}
        if complexes:
            params["complexes[]"] = complexes
        if buildings:
            params["buildings[]"] = buildings

        endpoints = [
            "list",
            "unassigned",
        ]

        async with httpx.AsyncClient() as client:
            tasks = [
                self._safe_request(client, f"/api/v1/storage/{e}", params)
                for e in endpoints
            ]
            results = await asyncio.gather(*tasks)

            return {
                "storage": {
                    endpoints[i]: results[i] for i in range(len(endpoints))
                }
            }

    async def get_news(
        self,
        complexes: list[int] | None = None,
        buildings: list[int] | None = None,
        type_: str | None = None,
    ) -> dict:
        params = {"token": self.token}
        if complexes:
            params["complexes[]"] = complexes
        if buildings:
            params["buildings[]"] = buildings
        if type_:
            params["types[]"] = [type_]

        async with httpx.AsyncClient() as client:
            res = await self._safe_request(client, "/api/v1/news/list", params)
            return {"news": {"all": res}}
