import pytest

pytestmark = pytest.mark.sphinx('html', testroot='categories')


@pytest.mark.parametrize('page', ['category1.html', ], indirect=True)
class TestCategoryPage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert 'Category 1' == content

    def test_not_in_nav(self, page):
        navitems = page.find_all('nav-item is-hidden-mobile')
        assert len(navitems) == 0

    def test_published(self, page):
        # YAML has published, in the past
        published = page.find(id='kb-sidenav-published-heading')
        heading = published.find(class_='menu-label').string.strip()
        assert 'Published' == heading
        pd = published.find_all('p')[1].contents[0].strip()
        assert '2015-04-25' in pd


@pytest.mark.parametrize('page', ['article1.html', ], indirect=True)
class TestReferringPage:
    def test_title(self, page):
        content = page.find('title').contents[0]
        assert 'Article 1' == content

    def test_published(self, page):
        categories = page.find(id='kb-sidenav-categories-heading')
        heading = categories.find(class_='menu-label').string.strip()
        assert 'Categories' == heading
        first_link = categories.find_all('a')[0]
        assert 'category1.html' == first_link.attrs['href']
        pd = first_link.find(class_='tag').contents[0].strip()
        assert 'category1' == pd

