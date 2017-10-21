import pytest

pytestmark = pytest.mark.sphinx('html', testroot='toctree')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestToctree:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Homepage'


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestDebugpage:
    def test_toctree(self, json_page):
        resources = json_page['site']['resources']
        homepage = resources['index']
        assert 'Test Homepage' == homepage['title']
        toctree = homepage['toctree']
        assert ['article1', 'article2', 'page1'] == toctree
