import pytest

pagepaths = ['index.html', 'articles/index.html', 'articles/article1.html']


# Home page
@pytest.mark.sphinx('html', testroot='articles')
@pytest.mark.parametrize('pagepath, expected', [
    ('index.html', 'Test Articles'),
    ('articles/index.html', 'Articles'),
    ('articles/article1.html', 'Article 1')
])
def test_titles(pages, pagepath, expected):
    content = pages[pagepath].find('title').contents[0]
    assert content == expected


@pytest.mark.sphinx('html', testroot='articles')
def test_section_appears_in_homepage(pages):
    page = pages['index.html']
    content = page.find(href='/articles').contents[0].strip()
    assert content == 'Articles'


@pytest.mark.sphinx('html', testroot='articles')
def test_section_appears_in_homepage(pages):
    page = pages['articles/index.html']
    content = page.find(href='article1.html').contents[0].strip()
    assert content == 'Article 1'


@pytest.mark.sphinx('html', testroot='articles')
def test_correct_content(pages):
    page = pages['articles/article1.html']
    section = page.find(id='article-1')
    content = section.find('p').contents[0].strip()
    assert content == 'Content after YAML.'
