import pytest

from kaybee.resources.base import (
    BaseResource, BaseResourceModel,
    BaseContainerModel
)
from kaybee.site import Site
from kaybee.site_config import SiteConfig


class Article(BaseResource):
    model = BaseResourceModel


class Homepage(BaseResource):
    model = BaseContainerModel


class Section(BaseResource):
    model = BaseContainerModel


@pytest.fixture()
def site_config():
    yield SiteConfig()


@pytest.fixture()
def dummy_resources():
    c0 = "published: 2015-01-01 01:23"
    c1 = """
in_nav: True
weight: 20
published: 2015-01-01 01:23
    """
    c2 = """
in_nav: True
weight: -10
published: 2015-01-01 01:23
    """
    c3 = """
published: 2015-01-01 01:23
in_nav: True    
    """

    s1 = Section('8783', 'section', c0)
    s1.title = 'The First'
    s2 = Section('1343', 'section', c0)
    s2.title = 'Second should sort ahead of first'
    s3 = Section('4675', 'section', c3)
    s3.title = 'Z Last weights first'
    s4 = Section('9856', 'section', c2)
    s4.title = 'Q Not Last No Weight'
    a1 = Article('4444', 'article', c1)
    a1.title = 'About'
    a2 = Article('23', 'article', 'in_nav: True')
    a2.title = 'Unpublished'
    yield (s1, s2, s3, s4, a1, a2,)


@pytest.fixture()
def dummy_resource(dummy_resources):
    yield dummy_resources[4]


@pytest.fixture()
def site(site_config, dummy_resources):
    s = Site(site_config)

    # Add some sample data
    for sr in dummy_resources:
        s.resources[sr.name] = sr
    yield s
