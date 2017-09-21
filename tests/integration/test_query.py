import pytest

pytestmark = pytest.mark.sphinx('html', testroot='queries')


@pytest.mark.parametrize('page', ['articles/index.html', ], indirect=True)
class TestQuery:
    def test_title(self, page):
        section = page.find(id='articles')
        heading = section.find('h2').contents[0]
        first_li = section.find_all('li')[0].contents[0]
        assert heading == 'Query Results'
        assert first_li == 'name: articles'
