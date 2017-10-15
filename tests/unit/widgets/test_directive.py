import pytest

from kaybee.core.core_type import CoreWidgetModel
from kaybee.widgets import BaseWidgetDirective
from kaybee.widgets.base import BaseWidget


class DummyWidgetModel(CoreWidgetModel):
    flag: int = None


class DummyWidget(BaseWidget):
    model = DummyWidgetModel


class SampleWidget:
    def __init__(self, name, kbtype, content):
        self.name = name
        self.kbtype = kbtype
        self.content = content
        self.props = dict(template='foo')


@pytest.fixture()
def base_widget():
    content = """
template: widget1.html
kbtype: section
    """
    yield DummyWidget('somewidget', 'dummywidget', content)


class SampleDirective(BaseWidgetDirective):
    pass


class Dummy:
    pass


class DummySite:
    def __init__(self):
        self.widgets = dict()


@pytest.fixture()
def dummy_directive(monkeypatch):
    monkeypatch.setattr(BaseWidgetDirective, 'get_widget_class',
                        lambda x: SampleWidget)
    monkeypatch.setattr(BaseWidgetDirective, 'docname', 'somedocname')
    monkeypatch.setattr(BaseWidgetDirective, 'widgets', dict())
    bd = SampleDirective('sample_directive', [], dict(), '', 0, 0, '', {}, {})

    yield bd


class TestBaseWidgetDirective:

    def test_import(self):
        assert BaseWidgetDirective.__name__ == 'BaseWidgetDirective'

    def test_construction(self, dummy_directive):
        assert 'sample_directive' == dummy_directive.name

    def test_construction_run(self, dummy_directive):
        result = dummy_directive.run()
        assert 'widget' == result[0].__class__.__name__

    def test_get_widget(self, dummy_directive):
        widget = dummy_directive.get_widget('dummy123')
        assert 'sample_directive' == widget.kbtype
