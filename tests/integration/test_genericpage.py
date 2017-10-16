import pytest

pytestmark = pytest.mark.sphinx('html', testroot='genericpage')


@pytest.mark.parametrize('page', ['genericpage1.html', ], indirect=True)
class TestGenericpage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Generic Page 1'

    def test_not_in_nav(self, page):
        navitems = page.find_all('nav-item is-hidden-mobile')
        assert 0 == len(navitems)

    def test_has_hero_style(self, page):
        div = page.find_all(class_='hero-body')
        assert 0 == len(div)
