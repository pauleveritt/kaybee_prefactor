import pytest

from kaybee.widgets import widget, BaseDirective, BaseWidget
from kaybee.widgets.querylist import QueryList

LOAD = 'kaybee.widgets.querylist.QueryList.load'


@pytest.fixture(name='query')
def dummy_query():
    content = """
template: query1.html
rtype: section    
    """
    yield QueryList(content)


class TestWidgetNode:

    def test_import(self):
        assert widget.__name__ == 'widget'


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

# def test_import():
#     assert QueryList.__name__ == 'QueryList'
#
#
# def test_instance(query):
#     expected = '{"rtype": "section", "template": "query1.html"}'
#     assert query.name == expected
#     assert query.props['template'] == 'query1.html'
#     assert query.props['rtype'] == 'section'
