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

    def test_name_sorted(self, base_widget: BaseWidget):
        expected = '{"kbtype": "section", "template": "widget1.html"}'
        assert base_widget.name == expected

    def test_template(self, base_widget: BaseWidget):
        assert base_widget.template == 'widget1.html'

    def test_render_rst(self, base_widget: BaseWidget):
        source = 'Hello *world*'
        result = base_widget.render_rst(source)
        assert '<div class="document">' in result
        assert '<p>Hello <em>world</em></p>' in result
        assert '</div>' in result
