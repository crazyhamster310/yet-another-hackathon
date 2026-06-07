import pytest
from unittest.mock import Mock 
from uuid import UUID

from app.domain.entites.screen import Template
from app.domain.entites.enums import WidgetType
@pytest.mark.unit
def test_template(client):
    template = Template(name="Template",widgettype=WidgetType.NEWS)
    assert isinstance(template.id,UUID)
    assert template.name = "Template"
    assert template.widgettype == WidgetType.NEWS
