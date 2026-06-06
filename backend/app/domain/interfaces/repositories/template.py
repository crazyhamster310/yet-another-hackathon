from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.screen import Template


class ITemplateRepository(ABC):
    @abstractmethod
    async def get_by_id(self, template_id: UUID) -> Template | None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Template]:
        pass

    @abstractmethod
    async def save(self, template: Template) -> Template:
        pass

    @abstractmethod
    async def delete(self, template_id: UUID) -> bool:
        pass
