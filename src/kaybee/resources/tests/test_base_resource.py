from resources.base_resource import BaseResource


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
    assert parent == 'sub'


def test_blog_sub_subsub_index():
    name, parent = BaseResource.parse_pagename('blog/sub/subsub/index')
    assert name == 'blog/sub/subsub'
    assert parent == 'sub'


def test_blog_sub_subsub_about():
    name, parent = BaseResource.parse_pagename('blog/sub/subsub/about')
    assert name == 'blog/sub/subsub/about'
    assert parent == 'subsub'
