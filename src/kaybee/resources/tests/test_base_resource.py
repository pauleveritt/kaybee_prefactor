import pytest
from resources.base_resource import BaseResource


class Node:
    parent = None
    props = {}

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


@pytest.fixture
def site():
    root = Node('root')
    f1 = Node('f1')
    f1.parent = '/'
    f2 = Node('f2')
    f2.parent = 'f1'
    f3 = Node('f3')
    f3.parent = 'f1/f2'
    f4 = Node('f4')
    f4.parent = 'f1/f2/f3'
    return {
        '/': root,
        'f1': f1,
        'f1/f2': f2,
        'f1/f2/f3': f3,
        'f1/f2/f3/f4': f4
    }


def fake_load(content):
    return dict(flag=9)


def test_import():
    assert BaseResource.__name__ == 'BaseResource'


def test_instance():
    BaseResource.load = fake_load
    br = BaseResource('index', 'rtype', 'title', 'content')
    assert br.name == '/'
    assert br.parent is None
    assert br.rtype == 'rtype'
    assert br.title == 'title'
    assert br.props['flag'] == 9


def test_index():
    name, parent = BaseResource.parse_pagename('index')
    assert name == '/'
    assert parent is None


def test_about():
    name, parent = BaseResource.parse_pagename('about')
    assert name == 'about'
    assert parent == '/'


def test_blog_index():
    name, parent = BaseResource.parse_pagename('blog/index')
    assert name == 'blog'
    assert parent == '/'


def test_blog_about():
    name, parent = BaseResource.parse_pagename('blog/about')
    assert name == 'blog/about'
    assert parent == 'blog'


def test_blog_sub_index():
    name, parent = BaseResource.parse_pagename('blog/sub/index')
    assert name == 'blog/sub'
    assert parent == 'blog'


def test_blog_sub_about():
    name, parent = BaseResource.parse_pagename('blog/sub/about')
    assert name == 'blog/sub/about'
    assert parent == 'blog/sub'


def test_blog_sub_subsub_index():
    name, parent = BaseResource.parse_pagename('blog/sub/subsub/index')
    assert name == 'blog/sub/subsub'
    assert parent == 'blog/sub'


def test_blog_sub_subsub_about():
    name, parent = BaseResource.parse_pagename('blog/sub/subsub/about')
    assert name == 'blog/sub/subsub/about'
    assert parent == 'blog/sub/subsub'


def test_blog_sub_subsub_s3_index():
    name, parent = BaseResource.parse_pagename('blog/sub/subsub/s3/index')
    assert name == 'blog/sub/subsub/s3'
    assert parent == 'blog/sub/subsub'


def test_blog_sub_subsub_s3_about():
    name, parent = BaseResource.parse_pagename('blog/sub/subsub/s3/about')
    assert name == 'blog/sub/subsub/s3/about'
    assert parent == 'blog/sub/subsub/s3'


def test_package_dir():
    assert BaseResource.package_dir().endswith('kaybee/resources')


def test_template():
    class Article(BaseResource):
        pass

    BaseResource.load = fake_load
    a = Article('index', 'rtype', 'title', 'content')
    assert a.template == 'article'


def test_root_index_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('index', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 0


def test_root_about_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('about', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 1


def test_f1_index_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/index', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 2


def test_f1_about_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/about', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 2


def test_f2_index_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/index', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 2


def test_f2_about_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/about', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 3


def test_f4_index_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/index', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 4


def test_f4_about_parents(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    parents = br.parents(site)
    assert len(parents) == 5


def test_find_prop_none(site):
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.findProp(site, 'foo')
    assert prop is None


def test_find_prop_self(site):
    site['f1/f2/f3/f4'].props['foo'] = 'hello4'
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.findProp(site, 'foo')
    assert prop == 'hello4'
    del site['f1/f2/f3/f4'].props['foo']


def test_find_prop_parent(site):
    site['f1/f2/f3'].props['foo'] = 'hello3'
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.findProp(site, 'foo')
    assert prop == 'hello3'
    del site['f1/f2/f3'].props['foo']


def test_find_prop_grandparent(site):
    site['f1/f2'].props['foo'] = 'hello2'
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.findProp(site, 'foo')
    assert prop == 'hello2'
    del site['f1/f2'].props['foo']


def test_find_prop_root(site):
    site['f1'].props['foo'] = 'hello1'
    BaseResource.load = fake_load
    br = BaseResource('f1/f2/f3/f4/about', 'rtype', 'title', 'content')
    prop = br.findProp(site, 'foo')
    assert prop == 'hello1'
    del site['f1'].props['foo']