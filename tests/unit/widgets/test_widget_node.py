import pytest

from kaybee.widgets.node import widget
from kaybee.widgets.base import BaseWidget, BaseWidgetModel


class DummyWidgetModel(BaseWidgetModel):
    flag: int = None


class DummyWidget(BaseWidget):
    model = DummyWidgetModel


class SampleWidget:
    def __init__(self, *args, **kw):
        self.name = 'name'
        self.props = dict(template='foo')


@pytest.fixture()
def base_widget():
    content = """
template: widget1.html
kbtype: section
    """
    yield DummyWidget('somewidget', 'dummywidget', content)


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'

    def test_construction(self, base_widget):
        assert base_widget.__class__.__name__ == 'DummyWidget'
