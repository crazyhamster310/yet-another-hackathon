from abc import ABC, abstractmethod
from typing import Dict

class IUjinProvider(ABC):
    
    @abstractmethod
    def get_news(self, complex_id: list[int] = None, building_id: list[int] = None, type_: list[str] = None) -> Dict:
        pass
    
    @abstractmethod
    def get_parking(self, complex_id: list[int] = None, building_id: list[int] = None) -> Dict:
        pass
    
    @abstractmethod
    def get_storage(self, complex_id: list[int] = None, building_id: list[int] = None) -> Dict:
        pass
    
    @abstractmethod
    def get_complexes(self) -> Dict:
        pass
    
    @abstractmethod
    def get_buildings(self, complex_id: list[int] = None) -> Dict:
        pass