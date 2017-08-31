import pytest
from pykwalify.errors import SchemaError
from kaybee.resources.base_resource import BaseResource

LOAD = 'kaybee.resources.base_resource.BaseResource.load'


class Node:
    parent = None
    rtype = ''

    def __init__(self, name):
        self.name = name
        self.props = {}

    def __repr__(self):
        return self.name


class DummyArticle(BaseResource):
    default_style = 'classstyle'


@pytest.fixture
def site():
    this_site = Node('site')
    f1 = Node('f1')
    f1.parent = '/'
    f1.props['doc_template'] = 'section_doctemplate.html'
    f1.props['style'] = 'sectionstyle'
    f2 = Node('f2')
    f2.parent = 'f1'
    f3 = Node('f3')
    f3.parent = 'f1/f2'
    f4 = Node('f4')
    f4.parent = 'f1/f2/f3'
    return {
        '/': this_site,
        'f1': f1,
        'f1/f2': f2,
        'f1/f2/f3': f3,
        'f1/f2/f3/f4': f4
    }


def test_import():
    assert BaseResource.__name__ == 'BaseResource'


def test_instance(monkeypatch):
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource('index', 'rtype', 'title', 'content')
    assert br.name == 'index'
    assert br.parent == '/'
    assert br.rtype == 'rtype'
    assert br.title == 'title'
    assert br.props['flag'] == 9


@pytest.mark.parametrize('loader, expected', [
    # Most specific: The YAML has a template
    (lambda c: dict(template='yamltemplate.html'), 'yamltemplate.html'),

    # Next specific, not in YAML, but in section
    (lambda c: dict(), 'section_doctemplate.html'),

    # Least specific: neither YAML nor section, get from class
    (lambda c: dict(flag=9), 'dummyarticle.html')
])
def test_template(monkeypatch, site, loader, expected):
    # In the last case, remove the doc_template from the dummy section
    # props
    if expected == 'dummyarticle.html':
        del site['f1'].props['doc_template']

    monkeypatch.setattr(LOAD, loader)
    a = DummyArticle('f1/f2/f3', 'rtype', 'title', 'content')
    assert a.template(site) == expected


@pytest.mark.parametrize('loader, expected', [
    # Most specific: The YAML has a style
    (lambda c: dict(style='yamlstyle'), 'yamlstyle'),

    # Next specific, not in YAML, but in parents
    (lambda c: dict(), 'sectionstyle'),

    # Least specific: neither YAML nor section, get from class
    (lambda c: dict(), 'classstyle')
])
def test_style(monkeypatch, loader, expected):
    s = site()
    if expected != 'sectionstyle':
        del s['f1'].props['style']

    monkeypatch.setattr(LOAD, loader)
    a = DummyArticle('f1/f2/f3', 'rtype', 'title', 'content')
    assert a.style(s) == expected


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
    monkeypatch.setattr(LOAD, lambda c: dict())
    br = BaseResource(pagename, 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == parents_len
    if pagename != '/':
        assert parents[0].name == parentname


@pytest.mark.parametrize('pagename, name, parent', [
    ('index', 'index', '/'),
    ('about', 'about', '/'),
    ('blog/index', 'blog', '/'),
    ('blog/about', 'blog/about', 'blog'),
    ('blog/s1/index', 'blog/s1', 'blog'),
    ('blog/s1/about', 'blog/s1/about', 'blog/s1'),
    ('blog/s1/s2/index', 'blog/s1/s2', 'blog/s1'),
    ('blog/s1/s2/about', 'blog/s1/s2/about', 'blog/s1/s2'),
    ('blog/s1/s2/s3/index', 'blog/s1/s2/s3', 'blog/s1/s2'),
    ('blog/s1/s2/s3/about', 'blog/s1/s2/s3/about', 'blog/s1/s2/s3'),
])
def test_name_parent(monkeypatch, site, pagename, name, parent):
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    this_name, this_parent = BaseResource.parse_pagename(pagename)
    assert this_name == name
    assert this_parent == parent


@pytest.mark.parametrize('parentname, propvalue', [
    (None, None),
    ('f1/f2/f3', 'hellof3'),
    ('f1/f2', 'hellof2'),
    ('f1', 'hellof1'),
    ('/', 'hellofsite'),
])
def test_find_prop_none(monkeypatch, site, parentname, propvalue):
    if parentname is not None:
        site[parentname].props['foo'] = propvalue
    monkeypatch.setattr(LOAD, lambda c: dict())
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.find_prop(site, 'foo')
    assert prop == propvalue
    if parentname is not None:
        del site[parentname].props['foo']


def test_package_dir():
    assert BaseResource.package_dir().endswith('kaybee/resources')


def test_schema_filename(monkeypatch):
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    assert br.schema_filename.endswith('resources/tests/dummyarticle')


def test_schema():
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    assert br.schema['mapping']['level']['enum'][0] == 1


def test_props():
    content = """
count: 999
level: 2
    """
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', content)
    assert br.props['count'] == 999
    assert br.props['level'] == 2


def test_validate_succeed():
    content = """
count: 999
level: 2
    """
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', content)
    br.validate(br.props, br.schema)


def test_validate_fail():
    content = """
xlevel: 2
    """
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', content)
    with pytest.raises(SchemaError) as excinfo:
        br.validate(br.props, br.schema)

    assert 'xlevel' in str(excinfo.value)


def test_empty_yaml_string():
    content = """
    
    
    """
    props = BaseResource.load(content)
    assert props == {}


def test_section_none(monkeypatch, site):
    monkeypatch.setattr(LOAD, lambda c: dict())
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    assert br.section(site) is None


def test_section_f1(monkeypatch, site):
    site['f1'].rtype = 'section'
    monkeypatch.setattr(LOAD, lambda c: dict())
    br = DummyArticle('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    assert br.section(site) == site['f1']


@pytest.mark.parametrize('pagename, nav_href, expected', [
    ('f1/index', 'f1', True),
    ('f1/index', 'f2', False),
    ('f1/about', 'f1', True),
    ('f1/about', 'f2', False),
    ('f1/f2/index', 'f1', True),
    ('f1/f2/about', 'f2', False),
])
def test_is_active(monkeypatch, site, pagename, nav_href, expected):
    monkeypatch.setattr(LOAD, lambda c: dict())
    br = DummyArticle(pagename, 'rtype', 'title', 'content')
    assert br.is_active_section(site, nav_href) == expected
