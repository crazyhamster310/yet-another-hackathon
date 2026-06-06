from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entities.enums import WidgetType


class TemplateDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    widget_type: WidgetType
    title: str
    content: str


class TemplateCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    widget_type: WidgetType
    title: str = Field(default="", max_length=255)
    content: str = Field(...)


class TemplateUpdateDTO(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    widget_type: WidgetType | None = None
    title: str | None = Field(None, max_length=255)
    content: str | None = None


class SlotDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slot_index: int = Field(..., ge=0, le=3)
    template: TemplateDTO | None = None


class ScreenReadDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    complex_id: int | None = None
    building_id: int | None = None
    is_emergency: bool
    emergency_text: str | None
    slots: dict[int, TemplateDTO | None]


class ScreenUpdateDTO(BaseModel):
    slug: str | None = Field(None, min_length=3, max_length=100)
    name: str | None = Field(None, min_length=1, max_length=255)
    complex_id: int | None = None
    building_id: int | None = None


class EmergencyUpdateDTO(BaseModel):
    is_emergency: bool
    emergency_text: str | None = None
    screen_ids: list[UUID] | None = None


class ScreenCreateDTO(BaseModel):
    slug: str = Field(..., min_length=3, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)
    complex_id: int | None = None
    building_id: int | None = None
