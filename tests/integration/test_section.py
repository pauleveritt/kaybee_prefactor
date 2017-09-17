import pytest

pagepaths = ['index.html', 'articles/index.html']


# Home page
@pytest.mark.sphinx('html', testroot='sections')
@pytest.mark.parametrize('pagepath, expected', [
    ('index.html', 'Test Sections'),
    ('articles/index.html', 'Articles')
])
def test_titles(pages, pagepath, expected):
    content = pages[pagepath].find('title').contents[0]
    assert content == expected


@pytest.mark.sphinx('html', testroot='sections')
def test_section_appears_in_homepage(pages):
    page = pages['index.html']
    content = page.find(href='/articles').contents[0].strip()
    assert content == 'Articles'


# Section page
@pytest.mark.sphinx('html', testroot='sections')
def test_section_appears_in_section(pages):
    page = pages['articles/index.html']
    content = page.find(href='article1.html').contents[0]
    assert 'Article 1' == content


@pytest.mark.sphinx('html', testroot='sections')
def test_correct_content(pages):
    page = pages['articles/index.html']
    section = page.find(id='articles')
    content = section.find('p').contents[0].strip()
    assert content == 'Content after YAML.'
