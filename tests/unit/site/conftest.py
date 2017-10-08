import pytest

from kaybee.core.site_config import SiteConfig
from kaybee.resources.article import Article
from kaybee.resources.section import Section
from kaybee.site import Site


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

    yield (
        Section('8783', 'section', 'The First', c0),
        Section('1343', 'section', 'Second should sort ahead of first', c0),
        Section('4675', 'section', 'Z Last weights first', c3),
        Section('9856', 'section', 'Q Not Last No Weight', c2),
        Article('4444', 'article', 'About', c1),
        Article('23', 'article', 'Unpublished', 'in_nav: True')
    )


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
