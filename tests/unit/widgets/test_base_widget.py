import pytest

from kaybee.widgets.base import BaseWidget, BaseWidgetModel


class DummyWidgetModel(BaseWidgetModel):
    flag: int = None


class DummyWidget(BaseWidget):
    model = DummyWidgetModel


@pytest.fixture()
def base_widget():
    content = """
template: widget1.html
kbtype: section
    """
    yield DummyWidget('somewidget', 'dummywidget', content)


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
