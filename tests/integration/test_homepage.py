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
