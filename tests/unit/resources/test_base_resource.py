import pytest

from kaybee.core.core_type import CoreType
from kaybee.resources import BaseResource
from kaybee.resources.article import Article


class Site:
    def __init__(self):
        self.resources = {}


@pytest.fixture
def site():
    f1 = Article('f1', 'article', 'Some Page', '')
    f1.props.doc_template = 'section_doctemplate.html'
    f1.props.style = 'sectionstyle'
    f2 = Article('f1/f2', 'article', 'Some Page', '')
    f3 = Article('f1/f2/f3', 'article', 'Some Page', '')
    f4 = Article('f1/f2/f3/f4', 'article', 'Some Page', '')
    s = Site()
    s.resources = {
        'f1': f1,
        'f1/f2': f2,
        'f1/f2/f3': f3,
        'f1/f2/f3/f4': f4
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


@pytest.fixture()
def dam(monkeypatch):
    """ Pretend to load and validate the model """
    dam = ArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    yield dam


@pytest.mark.parametrize('pagename, parents_len, parentname', [
    ('index', 0, 'site'),
    ('about', 0, 'site'),
    ('f1/index', 0, 'site'),
    ('f1/about', 1, 'f1'),
    ('f1/f2/index', 1, 'f1'),
    ('f1/f2/about', 2, 'f1/f2'),
    ('f1/f2/f3/index', 2, 'f1/f2'),
    ('f1/f2/f3/about', 3, 'f1/f2/f3'),
])
def test_root_parents(monkeypatch, site, pagename, parents_len, parentname,
                      dam):
    a = Article(pagename, 'kbtype', 'title', 'content')
    parents = a.parents(site)
    assert len(parents) == parents_len
    if parents_len:
        assert parentname == parents[0].name


def test_find_prop_none_local(monkeypatch, site, dam):
    a = Article('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    prop = a.find_prop(site, 'foo')
    assert prop is None


@pytest.mark.parametrize('parentname, propvalue', [
    ('f1/f2/f3', 'hellof3'),
    ('f1/f2', 'hellof2'),
    ('f1', 'hellof1'),
])
def test_find_prop_none(monkeypatch, site, dam, parentname, propvalue):
    site.resources[parentname].props.foo = propvalue
    a = Article('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    prop = a.find_prop(site, 'foo')
    assert prop == propvalue
    site.resources[parentname].props.foo = None


def test_section_none(monkeypatch, site, dam):
    a = Article('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    assert a.section(site) is None


def test_section_f1(monkeypatch, site, dam):
    site.resources['f1'].kbtype = 'section'
    a = Article('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    assert a.section(site) == site.resources['f1']


@pytest.mark.parametrize('pagename, nav_href, expected', [
    ('f1/index', 'f1', True),
    ('f1/index', 'f2', False),
    ('f1/about', 'f1', True),
    ('f1/about', 'f2', False),
    ('f1/f2/index', 'f1', True),
    ('f1/f2/about', 'f2', False),
])
def test_is_active(monkeypatch, site, dam, pagename, nav_href, expected):
    a = Article(pagename, 'kbtype', 'title', 'content')
    assert a.is_active_section(site, nav_href) == expected


#
# Inheriting template, style, etc.

@pytest.fixture()
def da():
    yield Article('f1/f2/f3', 'kbtype', 'title', 'content')


class TestInheritedProperty:

    def test_template_from_props(self, monkeypatch, site, dam, da):
        dam.template = 'damtemplate.html'
        assert da.template(site) == dam.template

    def test_template_from_section(self, monkeypatch, site, dam, da):
        assert da.template(site) == 'section_doctemplate.html'

    def test_template_from_class(self, monkeypatch, site, dam, da):
        # Delete the lineage-intheried doc_template prop on the section
        site.resources['f1'].props.doc_template = None
        assert da.template(site) == 'article.html'

    def test_style_from_props(self, monkeypatch, site, dam, da):
        dam.style = 'instance_style'
        assert da.style(site) == dam.style

    def test_style_from_section(self, monkeypatch, site, dam, da):
        assert da.style(site) == 'sectionstyle'

    def test_style_from_class(self, monkeypatch, site, dam, da):
        # Delete the lineage-intheried doc_template prop on the section
        site.resources['f1'].props.style = None
        assert da.style(site) == 'classstyle'
