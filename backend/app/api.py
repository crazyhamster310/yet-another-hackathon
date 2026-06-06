import requests
from typing import Dict

BASE_URL = "https://api-uae-test.ujin.tech"
TOKEN = ""
PER_PAGE = 1000

def get_complexes():
    data = {}
    data["complexes"] = requests.get(f"{BASE_URL}/api/v1/complex/list/",params={"token":TOKEN}).json()
    return data

def get_buildings():
    data = {}
    data["buildings"] = requests.get(f"{BASE_URL}/api/v1/buildings/get-list-crm/",params={"token":TOKEN,"per_page":PER_PAGE}).json()
    return data

def get_parking(complexes: list[int] | None, buildings: list[int] | None) -> Dict:
    data = {}
    params = {"token": TOKEN}
    if complexes:
        for complex_id in complexes:
            params["complexes[]"] = complex_id
    if buildings:
        for building_id in buildings:
            params["buildings[]"] = building_id
    
    data["parking"] = {"all": requests.get(f"{BASE_URL}/api/v1/parking/list",params=params).json(),
        "free": requests.get(f"{BASE_URL}/api/v1/parking/free",params=params).json(),
        "occupied": requests.get(f"{BASE_URL}/api/v1/parking/occupied",params=params).json(),
        "public": requests.get(f"{BASE_URL}/api/v1/parking/public",params=params).json(),
        "private": requests.get(f"{BASE_URL}/api/v1/parking/private",params=params).json(),
        "unassigned": requests.get(f"{BASE_URL}/api/v1/parking/unassigned",params=params).json()}
    
    return data

def get_storage(complexes: list[int] | None,buildings: list[int] | None) -> Dict:
    data = {}
    params = {"token": TOKEN}
    if complexes:
        for complex_id in complexes:
            params["complexes[]"] = complex_id
    if buildings:
        for building_id in buildings:
            params["buildings[]"] = building_id
    
    data["storage"] = {"all": requests.get(f"{BASE_URL}/api/v1/storage/list",params=params).json(),
        "free": requests.get(f"{BASE_URL}/api/v1/storage/free",params=params).json(),
        "occupied": requests.get(f"{BASE_URL}/api/v1/storage/occupied",params=params).json(),
        "public": requests.get(f"{BASE_URL}/api/v1/storage/public",params=params).json(),
        "private": requests.get(f"{BASE_URL}/api/v1/storage/private",params=params).json(),
        "unassigned": requests.get(f"{BASE_URL}/api/v1/storage/unassigned",params=params).json()}
    
    return data


def get_news(complexes: list[int] | None, buildings: list[int] | None) -> Dict:
    data = {}
    params = {"token": TOKEN}
    if complexes:
        for complex_id in complexes:
            params["complexes[]"] = complex_id
    if buildings:
        for building_id in buildings:
            params["buildings[]"] = building_id
    
    data["news"] = {"all": requests.get(f"{BASE_URL}/api/v1/news/list",params=params).json(),}
    
    return data