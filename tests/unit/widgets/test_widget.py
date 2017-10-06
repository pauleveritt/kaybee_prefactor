import pytest

from kaybee.core.core_type import CoreWidgetModel
from kaybee.widgets import widget, BaseDirective, BaseWidget


class DummyWidgetModel(CoreWidgetModel):
    flag: int = None


class DummyWidget(BaseWidget):
    model = DummyWidgetModel


@pytest.fixture(name='base_widget')
def dummy_base_widget():
    content = """
template: widget1.html
kbtype: section
    """
    yield DummyWidget('somewidget', 'dummywidget', 'Some Widget', content)


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'

    def test_construction(self, base_widget):
        assert base_widget.__class__.__name__ == 'DummyWidget'


class TestBaseDirective:

    def test_import(self):
        assert BaseDirective.__name__ == 'BaseDirective'


class TestBaseWidget:

    def test_import(self):
        assert BaseWidget.__name__ == 'BaseWidget'

    def test_construction(self):
        content = """
template: hello
                """
        dw = DummyWidget('somewidget', 'dummywidget', 'Some Widget', content)
        assert dw.__class__.__name__ == 'DummyWidget'
        assert dw.props.template == 'hello'

    def test_name_sorted(self, base_widget):
        expected = '{"kbtype": "section", "template": "widget1.html"}'
        assert base_widget.name == expected

    def test_template(self, base_widget):
        assert base_widget.template == 'widget1.html'
