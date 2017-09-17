import pytest

pagepaths = ['index.html']


# Home page
@pytest.mark.sphinx('html', testroot='homepage')
def test_titles(pages):
    content = pages['index.html'].find('title').contents[0]
    assert content == 'Test Homepage'


@pytest.mark.sphinx('html', testroot='homepage')
def test_not_in_nav(pages):
    page = pages['index.html']
    navitems = page.find_all('nav-item is-hidden-mobile')
    assert len(navitems) == 0


@pytest.mark.sphinx('html', testroot='homepage')
def test_has_hero_style(pages):
    page = pages['index.html']
    div = page.find_all(class_='hero-body')
    assert len(div) == 1

