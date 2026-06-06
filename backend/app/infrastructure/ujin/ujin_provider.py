import httpx
from typing import Dict
from ujin_provider import IUjinProvider

class UjinProvider(IUjinProvider):
        
    def __init__(self, token: str, base_url: str = "https://hck-api.unicorn.icu", per_page: int = 1000, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.per_page = per_page
        self.timeout = timeout
        
    def get_complexes(self) -> Dict:
        data = {}
        try:
            response = httpx.get(f"{self.base_url}/api/v1/complex/list/", params={"token": self.token}, timeout=self.timeout)
            response.raise_for_status()
            data["complexes"] = response.json()
        except httpx.HTTPStatusError as e:
            data["complexes"] = {"error": f"HTTP {e.response.status_code}", "details": str(e)}
        except Exception as e:
            data["complexes"] = {"error": "Request failed", "details": str(e)}
        return data

    def get_buildings(self, complexes: list[int] | None) -> Dict:
        data = {}
        params = {"token": self.token, "per_page": self.per_page}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        try:
            response = httpx.get(f"{self.base_url}/api/v1/buildings/get-list-crm/", params=params, timeout=self.timeout)
            response.raise_for_status()
            data["buildings"] = response.json()
        except httpx.HTTPStatusError as e:
            data["buildings"] = {"error": f"HTTP {e.response.status_code}", "details": str(e)}
        except Exception as e:
            data["buildings"] = {"error": "Request failed", "details": str(e)}
        return data

    def get_parking(self, complexes: list[int] | None, buildings: list[int] | None) -> Dict:
        data = {}
        params = {"token": self.token}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        if buildings:
            for building_id in buildings:
                params["buildings[]"] = building_id
        
        parking_data = {}
        endpoints = ["all", "free", "occupied", "public", "private", "unassigned"]
        
        for endpoint in endpoints:
            try:
                response = httpx.get(f"{self.base_url}/api/v1/parking/{endpoint}", params=params, timeout=self.timeout)
                response.raise_for_status()
                parking_data[endpoint] = response.json()
            except httpx.HTTPStatusError as e:
                parking_data[endpoint] = {"error": f"HTTP {e.response.status_code}", "details": str(e)}
            except Exception as e:
                parking_data[endpoint] = {"error": "Request failed", "details": str(e)}
        
        data["parking"] = parking_data
        return data

    def get_storage(self, complexes: list[int] | None, buildings: list[int] | None) -> Dict:
        data = {}
        params = {"token": self.token}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        if buildings:
            for building_id in buildings:
                params["buildings[]"] = building_id
        
        storage_data = {}
        endpoints = ["all", "free", "occupied", "public", "private", "unassigned"]
        
        for endpoint in endpoints:
            try:
                response = httpx.get(f"{self.base_url}/api/v1/storage/{endpoint}", params=params, timeout=self.timeout)
                response.raise_for_status()
                storage_data[endpoint] = response.json()
            except httpx.HTTPStatusError as e:
                storage_data[endpoint] = {"error": f"HTTP {e.response.status_code}", "details": str(e)}
            except Exception as e:
                storage_data[endpoint] = {"error": "Request failed", "details": str(e)}
        
        data["storage"] = storage_data
        return data
    def get_news(self, complexes: list[int] | None, buildings: list[int] | None, type_: list[str] | None) -> Dict:
        data = {}
        params = {"token": self.token}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        if buildings:
            for building_id in buildings:
                params["buildings[]"] = building_id
        if type_:
            for types in type_:
                params["types[]"] = types
        
        try:
            response = httpx.get(f"{self.base_url}/api/v1/news/list", params=params, timeout=self.timeout)
            response.raise_for_status()
            data["news"] = {"all": response.json()}
        except httpx.HTTPStatusError as e:
            data["news"] = {"all": {"error": f"HTTP {e.response.status_code}", "details": str(e)}}
        except Exception as e:
            data["news"] = {"all": {"error": "Request failed", "details": str(e)}}
        
        return data