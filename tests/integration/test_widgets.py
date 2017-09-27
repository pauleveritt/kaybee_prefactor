import pytest

pytestmark = pytest.mark.sphinx('html', testroot='widgets')


@pytest.mark.parametrize('page', ['index.html', ], indirect=True)
class TestHomepage:
    """ Normal querylist behavior """

    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Test Widgets'

    def test_headings(self, page):
        nodes = page.find_all(class_='panel-heading')
        assert len(nodes) == 3
        assert nodes[0].string.strip() == 'Recent Blog Posts'
        assert nodes[1].string.strip() == 'Recent Articles'
        assert nodes[2].string.strip() == 'Recent Tutorials'


@pytest.mark.parametrize('page', ['articles/index.html', ], indirect=True)
class TestSectionIndex:
    """ sectionquery widget """

    def test_title(self, page):
        content = page.find('title').string.strip()
        assert content == 'Articles'

    def test_sectionquery_results(self, page):
        value1 = page.find(id='kb-debug-result_count').string.strip()
        assert value1 == '1'
        value2 = page.find_all(class_='kb-debug-result')[0].string.strip()
        assert value2 == 'Article 5'


@pytest.mark.parametrize('page', ['articles/article1.html', ], indirect=True)
class TestArticle1:
    """ Widget with custom template """

    def test_title(self, page):
        content = page.find(id='kb-debug-widget').string.strip()
        assert content == 'Widget Custom Template'


@pytest.mark.parametrize('page', ['articles/article2.html', ], indirect=True)
class TestSectionArticle2:
    """ sectionquery widget """

    def test_title(self, page):
        content = page.find('title').string.strip()
        assert content == 'Article 2'

    def test_sectionquery_results(self, page):
        value1 = page.find(id='kb-debug-result_count').string.strip()
        assert value1 == '8'
        value2 = page.find_all(class_='kb-debug-result')[0].string.strip()
        assert value2 == 'Article 1'


@pytest.mark.parametrize('page', ['articles/article3.html', ], indirect=True)
class TestSectionArticle3:
    """ sectionquery widget """

    def test_title(self, page):
        content = page.find('title').string.strip()
        assert content == 'Article 3'

    def test_sectionquery_results(self, page):
        value1 = page.find(id='kb-debug-result_count').string.strip()
        assert value1 == '8'
        value2 = page.find_all(class_='kb-debug-result')[0].string.strip()
        assert value2 == 'ZZZ Article 4'


@pytest.mark.parametrize('page', ['articles/article4.html', ], indirect=True)
class TestSectionArticle4:
    """ sectionquery widget """

    def test_title(self, page):
        content = page.find('title').string.strip()
        assert content == 'ZZZ Article 4'

    def test_sectionquery_results(self, page):
        value1 = page.find(id='kb-debug-result_count').string.strip()
        assert value1 == '8'
        value2 = page.find_all(class_='kb-debug-result')[0].string.strip()
        assert value2 == 'Test Widgets'
