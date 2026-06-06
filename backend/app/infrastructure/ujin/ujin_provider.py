import requests
from typing import Dict
from app.domain.interfaces.providers.ujin_provider import IUjinProvider

class UjinProvider(IUjinProvider):
        
    def __init__(self, token: str, base_url_for_storage_parking: str = "https://hck-api.unicorn.icu", base_url_for_buildings_news_complex: str = "https://api-uae-test.ujin.tech", per_page: int = 1000):
        self.base_url_for_storage_parking = base_url_for_storage_parking.rstrip('/')
        self.base_url_for_buildings_news_complex = base_url_for_buildings_news_complex.rstrip('/')
        self.token = token
        self.per_page = per_page
        
    def get_complexes(self) -> Dict:
        data = {}
        data["complexes"] = requests.get(f"{self.base_url_for_buildings_news_complex}/api/v1/complex/list/",params={"token":self.token}).json()
        return data

    def get_buildings(self, complexes: list[int] | None) -> Dict:
        data = {}
        params = {"token": self.token, "per_page":self.per_page}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        data["buildings"] = requests.get(f"{self.base_url_for_buildings_news_complex}/api/v1/buildings/get-list-crm/",params=params).json()
        return data

    def get_parking(self,complexes: list[int] | None, buildings: list[int] | None) -> Dict:
        data = {}
        params = {"token": self.token}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        if buildings:
            for building_id in buildings:
                params["buildings[]"] = building_id
        
        data["parking"] = {"all": requests.get(f"{self.base_url_for_storage_parking}/api/v1/parking/list",params=params).json(),
            "free": requests.get(f"{self.base_url_for_storage_parking}/api/v1/parking/free",params=params).json(),
            "occupied": requests.get(f"{self.base_url_for_storage_parking}/api/v1/parking/occupied",params=params).json(),
            "public": requests.get(f"{self.base_url_for_storage_parking}/api/v1/parking/public",params=params).json(),
            "private": requests.get(f"{self.base_url_for_storage_parking}/api/v1/parking/private",params=params).json(),
            "unassigned": requests.get(f"{self.base_url_for_storage_parking}/api/v1/parking/unassigned",params=params).json()}
        
        return data

    def get_storage(self,complexes: list[int] | None,buildings: list[int] | None) -> Dict:
        data = {}
        params = {"token": self.token}
        if complexes:
            for complex_id in complexes:
                params["complexes[]"] = complex_id
        if buildings:
            for building_id in buildings:
                params["buildings[]"] = building_id
        
        data["storage"] = {"all": requests.get(f"{self.base_url_for_storage_parking}/api/v1/storage/list",params=params).json(),
            "free": requests.get(f"{self.base_url_for_storage_parking}/api/v1/storage/free",params=params).json(),
            "occupied": requests.get(f"{self.base_url_for_storage_parking}/api/v1/storage/occupied",params=params).json(),
            "public": requests.get(f"{self.base_url_for_storage_parking}/api/v1/storage/public",params=params).json(),
            "private": requests.get(f"{self.base_url_for_storage_parking}/api/v1/storage/private",params=params).json(),
            "unassigned": requests.get(f"{self.base_url_for_storage_parking}/api/v1/storage/unassigned",params=params).json()}
        
        return data

    def get_news(self,complexes: list[int] | None, buildings: list[int] | None, type_: list[str] | None) -> Dict:
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
        
        data["news"] = {"all": requests.get(f"{self.base_url_for_buildings_news_complex}/api/v1/news/list",params=params).json(),}
        
        return data