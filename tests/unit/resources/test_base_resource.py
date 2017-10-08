import pytest

from kaybee.resources import BaseResource
from kaybee.resources.article import Article
from kaybee.resources.section import Section


class Site:
    def __init__(self):
        self.resources = {}


@pytest.fixture
def site():
    f1_content = """
template: f1_section_template.html
overrides:
    article:
        template: override_article.html
    section:
        style: f1style    
    """
    about = Article('about', 'article', 'A1', '')
    f1 = Section('f1', 'section', 'S1', f1_content)
    f1_about = Article('f1/about', 'article', 'AF1', '')
    f2 = Section('f1/f2', 'section', 'S2', '')
    f2_about = Article('f1/f2/about', 'article', 'AF2', '')
    f3 = Section('f1/f2/f3', 'section', 'S3', 'style: f3style')
    f3_about = Article('f1/f2/f3/about', 'article', 'AF3', '')
    f4 = Article('f1/f2/f3/f4', 'article', 'A4', '')
    s = Site()
    s.resources = {
        'about': about,
        'f1': f1,
        'f1/about': f1_about,
        'f1/f2': f2,
        'f1/f2/about': f2_about,
        'f1/f2/f3': f3,
        'f1/f2/f3/about': f3_about,
        'f1/f2/f3/f4/index': f4
    }
    yield s


def test_import():
    assert BaseResource.__name__ == 'BaseResource'


def test_instance():
    da = Article('somepage', 'article', 'Some Page', '')
    assert da.__class__.__name__ == 'Article'
    assert da.pagename == 'somepage'
    assert da.name == 'somepage'
    assert da.parent == '/'
    assert da.kbtype == 'article'
    assert da.title == 'Some Page'
    assert da.props.in_nav is False


@pytest.mark.parametrize('pagename, parents_len, parentname', [
    ('about', 0, 'site'),
    ('f1', 0, 'site'),
    ('f1/about', 1, 'f1'),
    ('f1/f2', 1, 'f1'),
    ('f1/f2/about', 2, 'f1/f2'),
    ('f1/f2/f3', 2, 'f1/f2'),
    ('f1/f2/f3/about', 3, 'f1/f2/f3'),
])
def test_root_parents(site, pagename, parents_len, parentname):
    a = site.resources[pagename]
    parents = a.parents(site)
    assert parents_len == len(parents)
    if parents_len:
        assert parentname == parents[0].name


def test_find_prop_none_local(site):
    a = Article('f1/f2/f3/f4/about', 'kbtype', 'title', '')
    prop = a.find_prop(site, 'foo')
    assert None is prop


def test_section_nonesite(site):
    a = Article('f1/f2/f3/f4/about', 'kbtype', 'title', '')
    assert a.section(site) is None


def test_section_f1(site):
    a = Article('f1/f2/f3/another', 'kbtype', 'title', '')
    assert site.resources['f1/f2/f3'] == a.section(site)


@pytest.mark.parametrize('pagename, nav_href, expected', [
    ('f1/index', 'f1', True),
    ('f1/index', 'f2', False),
    ('f1/about', 'f1', True),
    ('f1/about', 'f2', False),
    ('f1/f2/index', 'f1', True),
    ('f1/f2/about', 'f2', False),
])
def test_is_active(site, pagename, nav_href, expected):
    a = Article(pagename, 'kbtype', 'title', '')
    assert a.is_active_section(site, nav_href) == expected


@pytest.fixture()
def da(site):
    yield site.resources['f1/f2/f3/about']


class TestInheritedProperty:

    def test_template_from_props(self, site, da):
        expected = 'f1_section_template.html'
        assert expected == site.resources['f1'].template(site)

    def test_template_from_section(self, site, da):
        expected = 'override_article.html'
        assert expected == da.template(site)

    def test_template_from_class(self, site, da):
        # Delete the lineage-intheried doc_template prop on the section
        f1 = site.resources['f1']
        del f1.props.overrides['article']
        assert 'article.html' == da.template(site)

    def test_style_from_props(self, site):
        da = site.resources['f1/f2/f3']
        assert 'f3style' == da.style(site)

    def test_style_from_section(self, site):
        da = site.resources['f1/f2']
        assert 'f1style' == da.style(site)

    def test_style_from_class(self, site):
        # Delete the lineage-inherited doc_template prop on the section
        del site.resources['f1'].props.overrides['section']
        da = site.resources['f1/f2']
        assert 'section.html' == da.style(site)


@pytest.mark.parametrize('content, expected', [
    ('', False),
    ('published: 2020-12-01 01:23', False),
    ('published: 2012-03-24 11:47', True),
])
def test_is_published(content, expected):
    article = Article('d1/a1', 'article', 'Some Article', content)
    assert expected is article.is_published()
