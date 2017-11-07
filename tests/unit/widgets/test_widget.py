import pytest

from kaybee.base_types import CoreWidgetModel
from kaybee.widgets import BaseWidgetDirective, widget
from kaybee.widgets.base import BaseWidget


class DummyWidgetModel(CoreWidgetModel):
    flag: int = None


class DummyWidget(BaseWidget):
    model = DummyWidgetModel


class SampleWidget:
    def __init__(self, *args, **kw):
        self.name = 'name'
        self.props = dict(template='foo')


@pytest.fixture(name='base_widget')
def dummy_base_widget():
    content = """
template: widget1.html
kbtype: section
    """
    yield DummyWidget('somewidget', 'dummywidget', content)


class SampleDirective(BaseWidgetDirective):
    name = 'sample_directive'


class SampleTocDirective(BaseWidgetDirective):
    name = 'sample_tocdirective'


class Dummy:
    pass


class DummySite:
    def __init__(self):
        self.widgets = dict()


@pytest.fixture()
def dummy_directive():
    bd = SampleDirective('', [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.site = DummySite()
    bd.state.document.settings.env.site.validator = Dummy()

    bd.state.document.settings.env.site.validator.validate = lambda x: True
    bd.state.document.settings.env.docname = 'xyz'
    bd.state.parent = Dummy()
    bd.state.parent.parent = Dummy()
    bd.config = Dummy()

    yield bd


@pytest.fixture()
def dummy_toc_directive():
    bd = SampleTocDirective('', [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.site = DummySite()
    bd.state.document.settings.env.site.validator = Dummy()

    bd.state.document.settings.env.site.validator.validate = lambda x: True
    bd.state.document.settings.env.docname = 'xyz'
    bd.state.parent = Dummy()
    bd.state.parent.parent = Dummy()
    bd.config = Dummy()

    yield bd


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'

    def test_construction(self, base_widget):
        assert base_widget.__class__.__name__ == 'DummyWidget'


class TestCategory:

    def test_import(self):
        assert BaseWidgetDirective.__name__ == 'BaseWidgetDirective'


class TestBaseWidget:

    def test_import(self):
        assert BaseWidget.__name__ == 'BaseWidget'

    def test_construction(self):
        content = """
template: hello
                """
        dw = DummyWidget('somewidget', 'dummywidget', content)
        assert dw.__class__.__name__ == 'DummyWidget'
        assert dw.props.template == 'hello'

    def test_name_sorted(self, base_widget):
        expected = '{"kbtype": "section", "template": "widget1.html"}'
        assert base_widget.name == expected

    def test_template(self, base_widget):
        assert base_widget.template == 'widget1.html'


class TestBaseWidgetDirective:

    def test_import(self):
        assert BaseWidgetDirective.__name__ == 'BaseWidgetDirective'

    def test_construction(self, dummy_directive):
        assert dummy_directive.run

    def test_construction_run(self, monkeypatch, dummy_directive):
        monkeypatch.setattr(BaseWidgetDirective, 'get_widget_class',
                            lambda x: SampleWidget)
        result = dummy_directive.run()
        assert 'widget' == result[0].__class__.__name__

