import pytest

from kaybee.core.core_type import CoreResourceModel, CoreType
from kaybee.resources import BaseResource


class Site:
    def __init__(self):
        self.resources = {}


class Node:
    parent = None
    kbtype = ''

    def __init__(self, name):
        self.name = name
        self.props = DummyArticleModel()

    def __repr__(self):
        return self.name


class DummyArticleModel(CoreResourceModel):
    doc_template: str = None
    foo: str = None


class DummyArticle(BaseResource):
    model = DummyArticleModel
    default_style = 'classstyle'


@pytest.fixture
def site():
    this_site = Node('site')
    f1 = Node('f1')
    f1.parent = '/'
    f1.props.doc_template = 'section_doctemplate.html'
    f1.props.style = 'sectionstyle'
    f2 = Node('f2')
    f2.parent = 'f1'
    f3 = Node('f3')
    f3.parent = 'f1/f2'
    f4 = Node('f4')
    f4.parent = 'f1/f2/f3'
    s = Site()
    s.resources = {
        '/': this_site,
        'f1': f1,
        'f1/f2': f2,
        'f1/f2/f3': f3,
        'f1/f2/f3/f4': f4
    }
    yield s


def test_import():
    assert BaseResource.__name__ == 'BaseResource'


def test_instance():
    da = DummyArticle('somepage', 'dummyarticle', 'Some Page', '')
    assert da.__class__.__name__ == 'DummyArticle'
    assert da.pagename == 'somepage'
    assert da.name == 'somepage'
    assert da.parent == '/'
    assert da.kbtype == 'dummyarticle'
    assert da.title == 'Some Page'
    assert da.props.in_nav is False


def test_template_from_props(monkeypatch, site):
    dam = DummyArticleModel()
    dam.template = 'damtemplate.html'
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3', 'kbtype', 'title', 'content')
    assert a.template(site) == dam.template


def test_template_from_section(monkeypatch, site):
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3', 'kbtype', 'title', 'content')
    assert a.template(site) == 'section_doctemplate.html'


def test_template_from_class(monkeypatch, site):
    # Delete the lineage-intheried doc_template prop on the section
    site.resources['f1'].props.doc_template = None
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3', 'kbtype', 'title', 'content')
    assert a.template(site) == 'dummyarticle.html'


def test_style_from_props(monkeypatch, site):
    dam = DummyArticleModel()
    dam.style = 'instance_style'
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3', 'kbtype', 'title', 'content')
    assert a.style(site) == dam.style


def test_style_from_section(monkeypatch, site):
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3', 'kbtype', 'title', 'content')
    assert a.style(site) == 'sectionstyle'


def test_style_from_class(monkeypatch, site):
    # Delete the lineage-intheried doc_template prop on the section
    site.resources['f1'].props.style = None
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3', 'kbtype', 'title', 'content')
    assert a.style(site) == 'classstyle'


@pytest.mark.parametrize('pagename, parents_len, parentname', [
    ('/', 0, None),
    ('index', 1, 'site'),
    ('about', 1, 'site'),
    ('f1/index', 1, 'site'),
    ('f1/about', 2, 'f1'),
    ('f1/f2/index', 2, 'f1'),
    ('f1/f2/about', 3, 'f2'),
    ('f1/f2/f3/index', 3, 'f2'),
    ('f1/f2/f3/about', 4, 'f3'),
])
def test_root_parents(monkeypatch, site, pagename, parents_len, parentname):
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: None)
    a = DummyArticle(pagename, 'kbtype', 'title', 'content')
    parents = a.parents(site)
    assert len(parents) == parents_len
    if pagename != '/':
        assert parents[0].name == parentname


def test_find_prop_none_local(monkeypatch, site):
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    prop = a.find_prop(site, 'foo')
    assert prop is None


@pytest.mark.parametrize('parentname, propvalue', [
    ('f1/f2/f3', 'hellof3'),
    ('f1/f2', 'hellof2'),
    ('f1', 'hellof1'),
    ('/', 'hellofsite'),
])
def test_find_prop_none(monkeypatch, site, parentname, propvalue):
    site.resources[parentname].props.foo = propvalue
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    prop = a.find_prop(site, 'foo')
    assert prop == propvalue
    site.resources[parentname].props.foo = None


def test_section_none(monkeypatch, site):
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    assert a.section(site) is None


def test_section_f1(monkeypatch, site):
    site.resources['f1'].kbtype = 'section'
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle('f1/f2/f3/f4/about', 'kbtype', 'title', 'content')
    assert a.section(site) == site.resources['f1']


@pytest.mark.parametrize('pagename, nav_href, expected', [
    ('f1/index', 'f1', True),
    ('f1/index', 'f2', False),
    ('f1/about', 'f1', True),
    ('f1/about', 'f2', False),
    ('f1/f2/index', 'f1', True),
    ('f1/f2/about', 'f2', False),
])
def test_is_active(monkeypatch, site, pagename, nav_href, expected):
    dam = DummyArticleModel()
    monkeypatch.setattr(CoreType, 'load_model', lambda s, m, c: dam)
    a = DummyArticle(pagename, 'kbtype', 'title', 'content')
    assert a.is_active_section(site, nav_href) == expected
