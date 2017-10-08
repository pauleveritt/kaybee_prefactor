import pytest

from kaybee.core.core_type import CorePropFilterModel
from kaybee.core.site_config import SiteConfig
from kaybee.resources.article import Article
from kaybee.resources.section import Section
from kaybee.site import Site


class DummyModel:
    sort_value = 'title'


class DummyQuery:

    def __init__(self, name):
        self.name = name
        self.props = DummyModel()


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
def dummy_widgets():
    # props = dict(template='query1.html', kbtype='section')
    dq = DummyQuery('query1')
    yield (
        dq,
        dq
        # DummyQuery(dict(template='query1.html', kbtype='section'))
    )


@pytest.fixture(name='sample_widget')
def dummy_widget(dummy_widgets):
    yield dummy_widgets[0]


@pytest.fixture()
def site(site_config, dummy_resources, dummy_widgets):
    s = Site(site_config)

    # Add some sample data
    for sr in dummy_resources:
        s.resources[sr.name] = sr
    for sw in dummy_widgets:
        s.widgets[sw.name] = sw
    yield s


def test_import():
    assert Site.__name__ == 'Site'


def test_construction(site):
    assert site.__class__.__name__ == 'Site'


def test_add_resource_succeeds(site, dummy_resource):
    site.resources[dummy_resource.name] = dummy_resource
    assert site.resources[dummy_resource.name] == dummy_resource


def test_remove_resource(site, dummy_resource):
    site.resources[dummy_resource.name] = dummy_resource
    del site.resources[dummy_resource.name]
    assert site.resources.get(dummy_resource.name, None) is None


def test_section_listing(site):
    assert 4 == len(site.sections)


@pytest.mark.parametrize('filter_key, filter_value, expected', [
    (None, 'article', 'About'),
    ('kbtype', 'article', 'About'),
    ('sort_value', 'title', 'About'),
    ('sort_value', 'weight', 'Q Not Last No Weight'),
    ('order', -1, 'Z Last weights first'),
])
def test_filter_resources(site, filter_key, filter_value, expected):
    # No filter applied
    if filter_key is None:
        kw = {}
    else:
        kw = {filter_key: filter_value}
    results = site.filter_resources(**kw)
    assert expected == results[0].title


def test_filter_resources_parent(site):
    published = 'published: 2015-01-01 01:23'
    parent = Section('section2/index', 'section', 'Section 2', published)
    child = Article('section2/article2', 'article', 'Resource 2', published)
    site.resources[parent.name] = parent
    site.resources[child.name] = child
    kw = dict(parent_name='section2')
    results = site.filter_resources(**kw)
    assert len(results) == 1
    assert results[0].title == 'Resource 2'


def test_filter_resources_props(site):
    prop = dict(key='weight', value=20)
    kv = [CorePropFilterModel(**prop)]
    kw = dict(props=kv)
    results = site.filter_resources(**kw)
    assert len(results) == 1
    assert results[0].title == 'About'


def test_filter_resources_limit(site):
    # No filter applied
    results = site.filter_resources(limit=2)
    assert len(results) == 2


@pytest.mark.parametrize('field, order, expected_title', [
    ('title', 1, 'About'),
    ('title', -1, 'Z Last weights first'),
])
def test_filter_resources_sort(site, field, order, expected_title):
    results = site.filter_resources(sort_value=field, order=order)
    first_title = results[0].title
    assert first_title == expected_title


def test_nav_menu(site, dummy_resources):
    # Only include things that want to be in the nav menu,
    # sorted by weight then by title

    navmenu_ids = [navmenu.name for navmenu in site.navmenu]
    assert 3 == len(navmenu_ids)
    assert navmenu_ids[0] == dummy_resources[3].name
    assert navmenu_ids[1] == dummy_resources[2].name
    assert navmenu_ids[2] == dummy_resources[4].name


def test_remove_widget(site, sample_widget):
    site.widgets[sample_widget.name] = sample_widget
    del site.widgets[sample_widget.name]
    assert site.widgets.get(sample_widget.name, None) is None


def test_is_debug(site):
    site.config.is_debug = False
    assert not site.is_debug
    site.config.is_debug = True
    assert site.is_debug
