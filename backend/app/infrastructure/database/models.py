import uuid

from sqlalchemy import (
    JSON,
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.domain.entities.enums import WidgetType


class Base(DeclarativeBase):
    pass


class TemplateModel(Base):
    __tablename__ = "templates"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255))
    widget_type: Mapped[WidgetType] = mapped_column(Enum(WidgetType))
    duration: Mapped[int] = mapped_column(Integer, default=15)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    content_rotation_settings: Mapped[dict] = mapped_column(JSON, default=dict)


class ScreenModel(Base):
    __tablename__ = "screens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))

    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False)
    emergency_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    slots = relationship(
        "ScreenSlotModel",
        back_populates="screen",
        cascade="all, delete-orphan",
        order_by="ScreenSlotModel.slot_index",
    )


class ScreenSlotModel(Base):
    __tablename__ = "screen_slots"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    screen_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("screens.id", ondelete="CASCADE"), index=True
    )
    template_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("templates.id", ondelete="SET NULL"), nullable=True
    )

    slot_index: Mapped[int] = mapped_column(Integer)

    screen = relationship("ScreenModel", back_populates="slots")
    template = relationship("TemplateModel")

    __table_args__ = (
        UniqueConstraint("screen_id", "slot_index", name="uq_screen_slot"),
    )
