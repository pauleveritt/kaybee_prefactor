import pytest

pytestmark = pytest.mark.sphinx('html', testroot='typedefs')


@pytest.mark.parametrize('json_page', ['debug.html', ], indirect=True)
class TestHomepage:
    def test_title(self, json_page):
        registry = json_page['registry']
        assert registry[0] == 1
