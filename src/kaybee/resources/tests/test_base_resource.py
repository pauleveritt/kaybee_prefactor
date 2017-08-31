import pytest
from pykwalify.errors import SchemaError
from kaybee.resources.base_resource import BaseResource

LOAD = 'kaybee.resources.base_resource.BaseResource.load'


class Node:
    parent = None
    props = {}

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class DummyArticle(BaseResource):
    pass


@pytest.fixture
def site():
    this_site = Node('site')
    f1 = Node('f1')
    f1.parent = '/'
    f1.props['doc_template'] = 'section_doctemplate'
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
    assert br.name == '/'
    assert br.parent is None
    assert br.rtype == 'rtype'
    assert br.title == 'title'
    assert br.props['flag'] == 9


def test_template_name_class(monkeypatch, site):
    # Get a template name when not in YAML
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    a = DummyArticle('index', 'rtype', 'title', 'content')
    assert a.template(site) == 'dummyarticle.html'


def test_template_name_from_yaml(monkeypatch, site):
    # Get a template name when the resource YAML overrides
    monkeypatch.setattr(LOAD, lambda c: dict(template='customtemplate.html'))
    a = DummyArticle('index', 'rtype', 'title', 'content')
    assert a.template(site) == 'customtemplate.html'


def test_template_name_from_section(monkeypatch, site):
    # Get a template name from a section
    monkeypatch.setattr(LOAD, lambda c: dict())
    a = DummyArticle('f1/f2/f3/index', 'rtype', 'title', 'content')
    assert a.template(site) == 'section_doctemplate'


@pytest.mark.parametrize('pagename, expected', [
    ('/', 0),
    ('index', 0),  ### This needs to be 1
    ('about', 1),
    ('f1/index', 1),
    ('f1/about', 2),
    ('f1/f2/index', 2),
    ('f1/f2/about', 3),
    ('f1/f2/f3/index', 3),
    ('f1/f2/f3/about', 4),
])
def test_root_parents(monkeypatch, site, pagename, expected):
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource(pagename, 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == expected


@pytest.mark.parametrize('pagename, name, parent', [
    ('index', '/', None),
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


###

def test_package_dir():
    assert BaseResource.package_dir().endswith('kaybee/resources')


def test_find_prop_none(monkeypatch, site):
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.find_prop(site, 'foo')
    assert prop is None


def test_find_prop_self(monkeypatch, site):
    site['f1/f2/f3/f4'].props['foo'] = 'hello4'
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.find_prop(site, 'foo')
    assert prop == 'hello4'
    del site['f1/f2/f3/f4'].props['foo']


def test_find_prop_parent(monkeypatch, site):
    site['f1/f2/f3'].props['foo'] = 'hello3'
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.find_prop(site, 'foo')
    assert prop == 'hello3'
    del site['f1/f2/f3'].props['foo']


def test_find_prop_grandparent(monkeypatch, site):
    site['f1/f2'].props['foo'] = 'hello2'
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.find_prop(site, 'foo')
    assert prop == 'hello2'
    del site['f1/f2'].props['foo']


def test_find_prop_root(monkeypatch, site):
    site['f1'].props['foo'] = 'hello1'
    monkeypatch.setattr(LOAD, lambda c: dict(flag=9))
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.find_prop(site, 'foo')
    assert prop == 'hello1'
    del site['f1'].props['foo']


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
