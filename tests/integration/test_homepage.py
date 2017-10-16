import pytest

pytestmark = pytest.mark.sphinx('html', testroot='homepage')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Homepage'

    def test_not_in_nav(self, page):
        navitems = page.find_all('nav-item is-hidden-mobile')
        assert len(navitems) == 0

    def test_has_hero_style(self, page):
        div = page.find_all(class_='hero-body')
        assert len(div) == 1


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestDebugpage:
    def test_title(self, json_page):
        registry = json_page['registry']
        resources = registry['resources']
        assert resources == ['article', 'category', 'homepage', 'section']
