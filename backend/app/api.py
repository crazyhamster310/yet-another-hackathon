import requests

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

def get_news():
    data = {}
    data["news"] = requests.get(f"{BASE_URL}/api/v1/news/list",params={"token":TOKEN}).json()
    return data