import pytest

pytestmark = pytest.mark.sphinx('html', testroot='querylists')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestQuery:
    def test_title(self, page):
        row = page.find(class_='row')
        columns = row.find_all(class_='column')
        assert len(columns) == 3
        headings = row.find_all(class_='panel-heading')
        assert headings[0].contents[0].strip() == 'Recent Blog Posts'
        assert headings[1].contents[0].strip() == 'Recent Articles'
        assert headings[2].contents[0].strip() == 'Recent Tutorials'


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestDebugpage:
    def test_title(self, json_page):
        registry = json_page['registry']
        resources = registry['resources']
        assert resources == ['article', 'category', 'homepage', 'section']
