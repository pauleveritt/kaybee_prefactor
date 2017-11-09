import pytest

pytestmark = pytest.mark.sphinx('html', testroot='customtypes')


@pytest.mark.parametrize('page', ['articles/article1.html', ], indirect=True)
class TestArticle1:
    """ Articles without properties set """

    def test_title(self, page):
        content = page.find('title').contents[0]
        assert 'Article 1' == content

    def test_correct_content(self, page):
        section = page.find(id='article-1')
        content = section.find('p').contents[0].strip()
        assert 'article1-body' in content

    def test_siteconfig_value(self, page):
        logo = page.find(id='siteconfig-logo')
        content = logo.contents[0].strip()
        assert 'xyz.png' in content

    def test_series(self, page):
        series_items = page.find_all(class_='article-series')
        assert 4 == len(series_items)
        first = series_items[0]
        assert 'Article 1' == first.string.strip()
        assert 'current' == first.attrs['data-current']
        assert '' == series_items[1].attrs['data-current']


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticle1Json:
    def test_docname(self, json_page):
        article = json_page['site']['resources']['articles/article1']
        assert 'articles/article1' == article['docname']

    def test_title(self, json_page):
        article = json_page['site']['resources']['articles/article1']
        assert 'Article 1' == article['title']

    def test_in_nav(self, json_page):
        article = json_page['site']['resources']['articles/article1']
        assert False is article['in_nav']

    def test_section(self, json_page):
        article = json_page['site']['resources']['articles/article1']
        assert 'articles/index' == article['section']

    def test_series(self, json_page):
        article = json_page['site']['resources']['articles/article1']
        series = article['series']
        first = series[0]
        second = series[1]
        assert 'Article 1' == first['title']
        assert True is first['current']
        assert 'Article 2' == second['title']
        assert False is second['current']


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticle2Json:
    def test_in_nav(self, json_page):
        article = json_page['site']['resources']['articles/article2']
        assert False is article['in_nav']

    def test_published(self, json_page):
        article = json_page['site']['resources']['articles/article2']
        assert '2099-01-01T01:23:00' == article['published']


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticle3Json:
    def test_weight(self, json_page):
        article = json_page['site']['resources']['articles/article3']
        assert 10 == article['weight']


@pytest.mark.parametrize('page', ['articles/article4.html', ], indirect=True)
class TestArticle4:
    def test_custom_heading(self, page):
        heading = page.find(class_='custom-heading').string.strip()
        assert 'Custom Article Template' == heading


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticle4Json:
    def test_in_nav(self, json_page):
        article = json_page['site']['resources']['articles/article4']
        assert True is article['in_nav']

    def test_weight(self, json_page):
        navmenu = json_page['site']['navmenu']
        assert 'articles/article4' == navmenu[0]

    def test_local_style(self, json_page):
        article = json_page['site']['resources']['articles/article4']
        assert 'local-style' == article['style']

    def test_custom_template(self, json_page):
        article = json_page['site']['resources']['articles/article4']
        assert 'article_custom_template.html' == article['template']


@pytest.mark.parametrize('page', ['articles2/article5.html', ],
                         indirect=True)
class TestArticle5:
    """ Custom template, direct style, lineage props """

    @pytest.mark.parametrize('propname, propvalue', [
        ('style', 'is-bold is-info'),
        # ('logo', 'some logo'),  # TODO Need a root with props
    ])
    def test_lineage_props(self, page, propname, propvalue):
        # No props
        node = page.find(id=f'kb-debug-lineage-{propname}')
        value = node.contents[0].strip()
        assert propvalue == value

    def test_custom_template(self, page):
        node = page.find(id='kb-debug-resource-template')
        value = node.contents[0].strip()
        assert value == 'article_custom_template2.html'


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestArticle5Json:
    def test_override_style(self, json_page):
        article = json_page['site']['resources']['articles2/article5']
        assert 'is-bold is-info' == article['style']

    def test_override_template(self, json_page):
        article = json_page['site']['resources']['articles2/article5']
        assert 'article_custom_template2.html' == article['template']


@pytest.mark.parametrize('page', ['genericpage1.html', ], indirect=True)
class TestGenericpage:
    def test_custom_heading(self, page):
        heading = page.find(class_='generic-page').string.strip()
        assert 'Generic Page' == heading


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestCategorypage:
    def test_categorypage(self, json_page):
        category = json_page['site']['resources']['category1']
        assert 'category1' == category['docname']

    def test_category(self, json_page):
        article = json_page['site']['resources']['articles/article1']
        references = article['references']
        assert 'category1' == references[0]
