import pytest

pytestmark = pytest.mark.sphinx('html', testroot='articles')


@pytest.mark.parametrize('page', ['articles/article1.html', ], indirect=True)
class TestArticle1:
    """ Articles without properties set """

    def test_title(self, page):
        content = page.find('title').contents[0]
        assert content == 'Article 1'

    def test_navmenu(self, page):
        # Not in
        menu = page.find(class_='nav-left')
        nav_items = menu.find_all(class_='nav-item')
        for ni in nav_items:
            content = ni.contents[0].strip()
            assert content != 'Article 1'

    def test_correct_content(self, page):
        section = page.find(id='article-1')
        content = section.find('p').contents[0].strip()
        assert 'article1-body' in content

    def test_published(self, page):
        # No published field in YAML
        published = page.find(id='kb-sidenav-published-heading')
        heading = published.find(class_='menu-label').string.strip()
        assert 'Draft' == heading


@pytest.mark.parametrize('page', ['articles/article2.html', ], indirect=True)
class TestArticle2:
    """ Articles with properties set """

    def test_navmenu(self, page):
        # Not in
        menu = page.find(class_='nav-left')
        nav_items = menu.find_all(class_='nav-item')
        for ni in nav_items:
            content = ni.contents[0].strip()
            assert content != 'Article 2'

    def test_published(self, page):
        # YAML has published, but in the far future
        published = page.find(id='kb-sidenav-published-heading')
        heading = published.find(class_='menu-label').string.strip()
        assert 'Draft' == heading


@pytest.mark.parametrize('json_page', ['debug_dump.json', ], indirect=True)
class TestJsonDebug:
    def test_article2(self, json_page):
        resources = json_page['site']['resources']
        article2 = resources['articles/article2']
        assert 'articles/article2' == article2['docname']
        assert False is article2['in_nav']
        assert 'Article 1' == article2['series'][0]['title']

    def test_article3(self, json_page):
        resources = json_page['site']['resources']
        article3 = resources['articles/article3']
        assert 'articles/article3' == article3['docname']
        assert 'articles/index' == article3['section']
        assert True is article3['in_nav']
        assert 10 == article3['weight']


@pytest.mark.parametrize('page', ['articles/article3.html', ], indirect=True)
class TestArticle3:
    """ Article in nav, but weighted later """

    def test_navmenu_position(self, page):
        # Not in
        menu = page.find(class_='nav-left')
        nav_items = menu.find_all(class_='nav-item')
        content = nav_items[3].contents[0].strip()
        assert content != 'Article 3'

    def test_published(self, page):
        # YAML has published, in the past
        published = page.find(id='kb-sidenav-published-heading')
        heading = published.find(class_='menu-label').string.strip()
        assert 'Published' == heading


@pytest.mark.parametrize('page', ['articles/article4.html', ], indirect=True)
class TestArticle4:
    """ Custom template, direct style, lineage props """

    def test_navmenu_position(self, page):
        # Not in
        menu = page.find(class_='nav-left')
        nav_items = menu.find_all(class_='nav-item')
        content = nav_items[1].contents[0].strip()
        assert content == 'Article 4'

    def test_local_style(self, page):
        node = page.find(id='kb-debug-resource-style')
        value = node.contents[0].strip()
        assert value == 'local-style'

    def test_custom_template(self, page):
        node = page.find(id='kb-debug-custom-title')
        value = node.contents[0].strip()
        assert value == 'some custom title'


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
        assert value == propvalue

    def test_custom_template(self, page):
        node = page.find(id='kb-debug-resource-template')
        value = node.contents[0].strip()
        assert value == 'article_custom_template2.html'
