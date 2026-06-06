from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.enums import WidgetType


class TemplateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    widget_type: WidgetType
    settings: dict
    content_rotation_settings: dict


class TemplateCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    widget_type: WidgetType
    settings: dict = Field(default_factory=dict)
    content_rotation_settings: dict = Field(default_factory=dict)


class SlotDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slot_index: int = Field(..., ge=0, le=3)
    template: TemplateDTO | None = None


class ScreenReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    is_emergency: bool
    emergency_text: str | None
    layout: dict[int, TemplateDTO | None]


class EmergencyUpdateDTO(BaseModel):
    is_emergency: bool
    emergency_text: str | None = None
    screen_ids: list[UUID] | None = None


class ScreenCreateDTO(BaseModel):
    slug: str = Field(..., min_length=3, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
