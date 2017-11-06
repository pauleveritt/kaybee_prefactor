import pytest

pytestmark = pytest.mark.sphinx('html', testroot='customtypes')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:

    def test_flag(self, page):
        content = page.find(id='hellowidget-flag').contents[0].strip()
        assert '456' == content

    def test_toctree(self, page):
        content = page.find(id='custom-toctree').contents[0].strip()
        assert 'Custom Toctree' == content


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestHomepageJson:
    def test_docname(self, json_page):
        widget = json_page['site']['widgets']['{"flag": 456}']
        assert 'index' == widget['docname']
        assert 'hellowidget' == widget['kbtype']
        assert '{"flag": 456}' == widget['name']
        assert None is widget['parent']

    def test_toctree(self, json_page):
        resources = json_page['site']['resources']
        articles = resources['articles/index']
        toctree = articles['toctree']
        items = ['articles/article1', 'articles/article2', 'articles/article3',
                 'articles/article4', ]
        assert items == toctree
