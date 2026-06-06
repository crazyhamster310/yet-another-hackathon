from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from .enums import WidgetType


class Template(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    name: str
    widget_type: WidgetType
    duration: int = 15
    settings: dict = Field(default_factory=dict)


class Screen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    slug: str
    name: str

    is_emergency: bool = False
    emergency_text: str | None = None

    playlist: list[Template] = Field(default_factory=list)
