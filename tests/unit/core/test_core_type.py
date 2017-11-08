from json import loads

import datetime
import pytest
from pydantic import ValidationError
from pydantic.main import BaseModel

from kaybee.base_types import (
    CoreType,
    ReferencesType
)
from kaybee.resources.base import BaseContainerModel, BaseResourceModel


class DummyMissingModel(CoreType):
    pass


class DummyArticleModel(BaseModel):
    in_nav: bool = False
    weight: int = 0


class DummyArticle(CoreType):
    kind = 'resource'
    model = DummyArticleModel


class DummyContainerModel(BaseContainerModel):
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
        da = DummyArticle('someparent/somepage', 'dummyarticle', '')
        assert da.__class__.__name__ == 'DummyArticle'
        assert da.docname == 'someparent/somepage'
        assert da.name == 'someparent/somepage'
        assert da.parent == 'someparent/index'
        assert da.kbtype == 'dummyarticle'
        assert da.props.in_nav is False

    def test_widget_name_construction(self):
        yaml_content = """
in_nav: True
weight: 998
        """

        dw = DummyWidget('someparent/somepage', 'dummyarticle', yaml_content)
        assert dw.name == '{"in_nav": true, "weight": 998}'

    def test_missing_model(self):
        with pytest.raises(AttributeError) as exc:
            DummyMissingModel('somepage', 'dummyarticle', '')
        v = "Class DummyMissingModel must have model attribute"
        assert v == str(exc.value)

    def test_failed_validation(self):
        yaml_content = '''
weight: 'Should Fail'        
        '''
        with pytest.raises(ValidationError) as exc:
            DummyArticle('somepage', 'dummyarticle', yaml_content)
        error = loads(exc.value.json())['weight']['error_msg']
        expected = "invalid literal for int() with base 10: 'Should Fail'"
        assert error == expected

    @pytest.mark.parametrize('docname, parent', [
        ('index', None),
        ('about', 'index'),
        ('blog/index', 'index'),
        ('blog/about', 'blog/index'),
        ('blog/s1/index', 'blog/index'),
        ('blog/s1/about', 'blog/s1/index'),
        ('blog/s1/s2/index', 'blog/s1/index'),
        ('blog/s1/s2/about', 'blog/s1/s2/index'),
        ('blog/s1/s2/s3/index', 'blog/s1/s2/index'),
        ('blog/s1/s2/s3/about', 'blog/s1/s2/s3/index'),
    ])
    def test_parse_parent(self, site, docname, parent):
        this_parent = CoreType.parse_parent(docname)
        assert parent == this_parent


class TestResource:
    def test_published_date(self):
        past = BaseResourceModel(**dict(published='2017-06-01 12:22'))
        future = BaseResourceModel(**dict(published='2020-11-27 01:43'))
        no_date = BaseResourceModel(**dict())
        now = datetime.datetime.now()
        assert None is no_date.published
        assert now > past.published
        assert now < future.published

    def test_category(self):
        no_cats = BaseResourceModel(**dict(category=[]))
        assert [] == no_cats.category
        c1 = ['python', 'web']
        cats = BaseResourceModel(**dict(category=c1))
        assert c1 == cats.category
        c2 = [923, dict(broken=True)]
        with pytest.raises(ValidationError):
            BaseResourceModel(**dict(category=c2))


class TestContainer:
    def test_import(self):
        assert BaseContainerModel.__name__ == 'BaseContainerModel'

    def test_construction(self):
        content = """
        
        """
        dc = DummyContainer(
            'someparent/somepage', 'dummycontainer', content)
        assert dc.docname == 'someparent/somepage'

    def test_overrides(self):
        content = """
overrides:
    article:
        template: sometemplate2.html
        """
        dc = DummyContainer(
            'someparent/somepage', 'dummycontainer', content)
        overrides = dc.props.overrides
        assert overrides['article']['template'] == 'sometemplate2.html'


class TestReferenceType:
    def test_import(self):
        assert 'ReferencesType' == ReferencesType.__name__

    def test_valid(self):
        tags = ['tag1', 'tag2']
        article = BaseResourceModel(**dict(tag=tags))
        assert tags == article.tag

    def test_invalid(self):
        tags = ['tag1', 9]
        with pytest.raises(ValidationError):
            BaseResourceModel(**dict(tag=tags))
