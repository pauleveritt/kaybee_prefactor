from json import loads

import pytest
from pydantic import ValidationError
from pydantic.main import BaseModel

from kaybee.core.core_type import CoreType, CoreContainerModel


class DummyMissingModel(CoreType):
    pass


class DummyArticleModel(BaseModel):
    in_nav: bool = False
    weight: int = 0


class DummyArticle(CoreType):
    kind = 'resource'
    model = DummyArticleModel


class DummyContainerModel(CoreContainerModel):
    pass


class DummyContainer(CoreType):
    kind = 'resource'
    model = DummyContainerModel


class DummyWidget(CoreType):
    kind = 'widget'
    model = DummyArticleModel


class Site:
    def __init__(self):
        self.resources = {}


class Node:
    parent = None
    kbtype = ''

    def __init__(self, name):
        self.name = name
        self.props = {}

    def __repr__(self):
        return self.name


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
    s = Site()
    s.resources = {
        '/': this_site,
        'f1': f1,
        'f1/f2': f2,
        'f1/f2/f3': f3,
        'f1/f2/f3/f4': f4
    }
    yield s


class TestCoreType:
    def test_import(self):
        assert CoreType.__name__ == 'CoreType'

    def test_subclass_and_construct(self):
        da = DummyArticle('someparent/somepage', 'dummyarticle', 'Some Page',
                          '')
        assert da.__class__.__name__ == 'DummyArticle'
        assert da.pagename == 'someparent/somepage'
        assert da.name == 'someparent/somepage'
        assert da.parent == 'someparent'
        assert da.kbtype == 'dummyarticle'
        assert da.title == 'Some Page'
        assert da.props.in_nav is False

    def test_widget_name_construction(self):
        yaml_content = """
in_nav: True
weight: 998
        """

        dw = DummyWidget('someparent/somepage', 'dummyarticle', 'Some Page',
                         yaml_content)
        assert dw.name == '{"in_nav": true, "weight": 998}'

    def test_missing_model(self):
        with pytest.raises(AttributeError) as exc:
            DummyMissingModel('somepage', 'dummyarticle', 'Some Page', '')
        v = "'DummyMissingModel' object has no attribute 'model'"
        assert v == str(exc.value)

    def test_failed_validation(self):
        yaml_content = '''
weight: 'Should Fail'        
        '''
        with pytest.raises(ValidationError) as exc:
            DummyArticle('somepage', 'dummyarticle', 'Some Page',
                         yaml_content)
        error = loads(exc.value.json())['weight']['error_msg']
        expected = "invalid literal for int() with base 10: 'Should Fail'"
        assert error == expected


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
def test_name_parent(site, pagename, name, parent):
    this_name, this_parent = CoreType.parse_pagename(pagename)
    assert this_name == name
    assert this_parent == parent


class TestContainer:
    def test_import(self):
        assert CoreContainerModel.__name__ == 'CoreContainerModel'

    def test_construction(self):
        content = """
        
        """
        dc = DummyContainer(
            'someparent/somepage', 'dummycontainer', 'Some Page', content)
        assert dc.pagename == 'someparent/somepage'

    def test_overrides(self):
        content = """
overrides:
    article:
        template: sometemplate2.html
        """
        dc = DummyContainer(
            'someparent/somepage', 'dummycontainer', 'Some Page', content)
        overrides = dc.props.overrides
        assert overrides['article']['template'] == 'sometemplate2.html'
