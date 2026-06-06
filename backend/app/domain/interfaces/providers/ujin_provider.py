from abc import ABC, abstractmethod
from typing import Dict

class IUjinProvider(ABC):
    
    @abstractmethod
    def get_news(self, complexes: list[int] = None, buildings: list[int] = None, type_: str = None) -> Dict:
        pass
    
    @abstractmethod
    def get_parking(self, complexes: list[int] = None, buildings: list[int] = None) -> Dict:
        pass
    
    @abstractmethod
    def get_storage(self, complexes: list[int] = None, buildings: list[int] = None) -> Dict:
        pass
    
    @abstractmethod
    def get_complexes(self) -> Dict:
        pass
    
    @abstractmethod
    def get_buildings(self, complexes: list[int] = None) -> Dict:
        pass