import pytest

pytestmark = pytest.mark.sphinx('html', testroot='typedefs')


@pytest.mark.parametrize('json_page', ['debug.html', ], indirect=True)
class TestDebugpage:
    def test_title(self, json_page):
        registry = json_page['registry']
        resources = registry['resources']
        assert resources == ['blogpost', 'article', 'homepage', 'section',
                             'customsection']
