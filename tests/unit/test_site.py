import pytest
from copy import deepcopy

from kaybee.decorators import kb
from kaybee.site import Site


class DummyResource:
    parent = None
    rtype = 'resource'

    def __init__(self, name, title, in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )


class DummySection:
    rtype = 'section'

    def __init__(self, name, title,
                 in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )

    def __str__(self):
        return self.name


class DummyQuery:

    def __init__(self, name, props):
        self.name = name
        self.props = props


@pytest.fixture()
def site_config():
    yield dict()


@pytest.fixture(name='sample_resources')
def dummy_resources():
    yield (
        DummySection('8783', 'The First', in_nav=True),
        DummySection('1343', 'Second should sort ahead of first'),
        DummySection('4675', 'Z Last weights first', in_nav=True),
        DummySection('9856', 'Q Not Last No Weight', in_nav=True, weight=-10),
        DummyResource('4444', 'About', in_nav=True, weight=20)
    )


@pytest.fixture(name='sample_resource')
def dummy_resource(sample_resources):
    yield sample_resources[4]


@pytest.fixture(name='sample_widgets')
def dummy_widgets():
    props = dict(template='query1.html', rtype='section')
    dq = DummyQuery('query1', props)
    yield (
        dq,
        dq
        # DummyQuery(dict(template='query1.html', rtype='section'))
    )

@pytest.fixture(name='sample_widget')
def dummy_widget(sample_widgets):
    yield sample_widgets[0]


@pytest.fixture()
def site(site_config, sample_resources, sample_widgets):
    original_config = deepcopy(kb.config)
    s = Site(site_config)
    kb.config.resources = dict()
    kb.config.widgets = dict()

    # Register some classes
    kb.config.resources['dummyresource'] = DummyResource
    kb.config.resources['dummysection'] = DummySection
    kb.config.resources['dummyquery'] = DummyQuery
    kb.config.widgets['dummyquery'] = DummyQuery

    # Add some sample data
    [s.add_resource(sr) for sr in sample_resources]
    [s.add_widget(sw) for sw in sample_widgets]
    yield s

    # Reset kb.config
    kb.config = original_config


def test_import():
    assert Site.__name__ == 'Site'


def test_construction(site):
    assert site.__class__.__name__ == 'Site'


def test_add_resource_succeeds(site, sample_resource):
    site.add_resource(sample_resource)
    assert site.resources.get(sample_resource.name) == sample_resource


def test_remove_resource(site, sample_resource):
    site.add_resource(sample_resource)
    site.remove_resource(sample_resource.name)
    assert site.resources.get(sample_resource.name, None) is None


def test_section_listing(site, sample_resources):
    assert len(site.sections) == len(sample_resources) - 1


@pytest.mark.parametrize('filter_key, filter_value, expected', [
    (None, 'resource', 'About'),
    ('rtype', 'resource', 'About'),
    ('sort_value', 'title', 'About'),
    ('sort_value', 'weight', 'Q Not Last No Weight'),
    ('order', -1, 'Z Last weights first')
])
def test_filter_resources(site, filter_key, filter_value, expected):
    # No filter applied
    if filter_key is None:
        kw = {}
    else:
        kw = {filter_key: filter_value}
    results = site.filter_resources(**kw)
    assert results[0].title == expected


def test_filter_resources_limit(site):
    # No filter applied
    results = site.filter_resources(limit=2)
    assert len(results) == 2


def test_nav_menu(site, sample_resources):
    # Only include things that want to be in the nav menu,
    # sorted by weight then by title

    navmenu_ids = [navmenu.name for navmenu in site.navmenu]
    assert navmenu_ids[0] == sample_resources[3].name
    assert navmenu_ids[1] == sample_resources[0].name
    assert navmenu_ids[2] == sample_resources[2].name
    assert navmenu_ids[3] == sample_resources[4].name


def test_validator_exists(site):
    assert site.validator.__class__.__name__ == 'Validator'


def test_remove_widget(site, sample_widget):
    site.add_widget(sample_widget)
    site.remove_widget(sample_widget.name)
    assert site.widgets.get(sample_widget.name, None) is None
