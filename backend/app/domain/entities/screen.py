from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

from .enums import WidgetType


class Template(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    name: str
    widget_type: WidgetType
    settings: dict = Field(default_factory=dict)
    content_rotation_settings: dict = Field(default_factory=dict)


class Screen(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    slug: str
    name: str

    complex_id: int | None = None
    building_id: int | None = None

    is_emergency: bool = False
    emergency_text: str | None = None

    layout: dict[int, Template | None] = Field(
        default_factory=lambda: {0: None, 1: None, 2: None, 3: None}
    )

    def assign_template(self, slot_index: int, template: Template):
        if 0 <= slot_index <= 3:
            self.layout[slot_index] = template