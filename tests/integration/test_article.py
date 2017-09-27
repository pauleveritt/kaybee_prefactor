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

    @pytest.mark.parametrize('propname, propvalue', [
        ('in_nav', None),
        ('weight', None),
    ])
    def test_direct_props(self, page, propname, propvalue):
        # No props
        node = page.find(id=f'kb-debug-resource-props-{propname}-value')
        assert node == propvalue


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

    @pytest.mark.parametrize('propname, propvalue', [
        ('in_nav', 'False'),
    ])
    def test_direct_props(self, page, propname, propvalue):
        # No props
        node = page.find(id=f'kb-debug-resource-props-{propname}-value')
        value = node.contents[0].strip()
        assert value == propvalue


@pytest.mark.parametrize('page', ['articles/article3.html', ], indirect=True)
class TestArticle3:
    """ Article in nav, but weighted later """

    def test_navmenu_position(self, page):
        # Not in
        menu = page.find(class_='nav-left')
        nav_items = menu.find_all(class_='nav-item')
        content = nav_items[3].contents[0].strip()
        assert content != 'Article 3'

    def test_style(self, page):
        node = page.find(id='kb-debug-resource-style')
        value = node.contents[0].strip()
        assert value == 'is-bold is-info'

    def test_section_name(self, page):
        node = page.find(id='kb-debug-resource-section')
        value = node.contents[0].strip()
        assert value == 'articles'

    @pytest.mark.parametrize('propname, propvalue', [
        ('in_nav', 'True'),
        ('weight', '10'),
    ])
    def test_direct_props(self, page, propname, propvalue):
        # No props
        node = page.find(id=f'kb-debug-resource-props-{propname}-value')
        value = node.contents[0].strip()
        assert value == propvalue


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

