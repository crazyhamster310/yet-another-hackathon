from abc import ABC, abstractmethod


class IUjinProvider(ABC):
    @abstractmethod
    async def get_news(
        self,
        complexes: list[int] | None = None,
        buildings: list[int] | None = None,
        type_: str = None,
    ) -> dict:
        pass

    @abstractmethod
    async def get_parking(
        self,
        complexes: list[int] | None = None,
        buildings: list[int] | None = None,
    ) -> dict:
        pass

    @abstractmethod
    async def get_storage(
        self,
        complexes: list[int] | None = None,
        buildings: list[int] | None = None,
    ) -> dict:
        pass

    @abstractmethod
    async def get_complexes(self) -> dict:
        pass

    @abstractmethod
    async def get_buildings(self, complexes: list[int] | None = None) -> dict:
        pass
