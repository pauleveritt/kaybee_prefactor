import pytest

pytestmark = pytest.mark.sphinx('html', testroot='articles')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Articles'

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

    def test_not_in_navmenu(self, page):
        menu = page.find(class_='nav-left')
        nav_items = menu.find_all(class_='nav-item')
        for ni in nav_items:
            assert ni.contents[0].strip() != 'Article 1'

    def test_correct_content(self, page):
        section = page.find(id='article-1')
        content = section.find('p').contents[0].strip()
        assert content == 'Content after YAML.'


@pytest.mark.parametrize('page', ['articles/article2.html', ], indirect=True)
class TestArticleNav:
    def test_navmenu_href(self, page):
        menu = page.find(class_='nav-left')
        nav_item = menu.find_all(class_='nav-item')
        value = nav_item[2].contents[0].strip()
        assert value == 'Article 2'

# @pytest.mark.parametrize('page', ['articles/article3.html', ], indirect=True)
# class TestArticleTemplate:
#     def test_template(self, page):
#         title = page.find('title')
#         assert title.contents[0].strip() == 'Article 2'

