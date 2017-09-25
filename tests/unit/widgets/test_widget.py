import pytest

from kaybee.widgets import widget, BaseDirective, BaseWidget


@pytest.fixture(name='base_widget')
def dummy_base_widget():
    content = """
template: widget1.html
rtype: section
    """
    yield BaseWidget(content)


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'

    def test_construction(self, base_widget):
        assert base_widget.__class__.__name__ == 'BaseWidget'


class TestBaseDirective:

    def test_import(self):
        assert BaseDirective.__name__ == 'BaseDirective'


class TestBaseWidget:

    def test_import(self):
        assert BaseWidget.__name__ == 'BaseWidget'

    def test_construction(self):
        content = """
flag: 9        
        """
        bw = BaseWidget(content)
        assert bw.content == content
        assert bw.props['flag'] == 9

    def test_name_sorted(self, base_widget):
        # Do the props one way
        expected = '{"limit": 5, "rtype": "section"}'
        base_widget.props = {'rtype': 'section', 'limit': 5}
        assert base_widget.name == expected
        base_widget.props = {'limit': 5, 'rtype': 'section'}
        assert base_widget.name == expected

    def test_template(self, base_widget):
        assert base_widget.template == 'widget1.html'
