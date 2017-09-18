import pytest

pytestmark = pytest.mark.sphinx('html', testroot='sections')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Sections'

    def test_section_appears_in_homepage(self, page):
        content = page.find(href='/articles').contents[0].strip()
        assert content == 'Articles'


@pytest.mark.parametrize('page', ['articles/index.html', ], indirect=True)
class TestSection:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Articles'

    def test_section_appears_in_homepage(self, page):
        content = page.find(href='article1.html').contents[0].strip()
        assert content == 'Article 1'


@pytest.mark.parametrize('page', ['articles/article1.html', ], indirect=True)
class TestArticle:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Article 1'

    def test_correct_content(self, page):
        section = page.find(id='article-1')
        content = section.find('p').contents[0].strip()
        assert content == 'Content after YAML.'
