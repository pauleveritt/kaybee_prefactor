import pytest

from kaybee.core.core_type import CorePropFilterModel
from kaybee.site import Site


class DummyModel:
    sort_value = 'title'


class DummyResource:
    parent = None
    kbtype = 'resource'

    def __init__(self, name, title, in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = DummyModel()
        self.props.in_nav = in_nav
        self.props.weight = weight
        self._parents = []

    def parents(self, site):
        return self._parents


class DummySection:
    kbtype = 'section'

    def __init__(self, name, title,
                 in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = DummyModel()
        self.props.in_nav = in_nav
        self.props.weight = weight

        self._parents = []

    def parents(self, site):
        return self._parents

    def __str__(self):
        return self.name


class DummyQuery:

    def __init__(self, name):
        self.name = name
        self.props = DummyModel()


@pytest.fixture()
def site_config():
    yield DummyModel()


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
    # props = dict(template='query1.html', kbtype='section')
    dq = DummyQuery('query1')
    yield (
        dq,
        dq
        # DummyQuery(dict(template='query1.html', kbtype='section'))
    )


@pytest.fixture(name='sample_widget')
def dummy_widget(sample_widgets):
    yield sample_widgets[0]


@pytest.fixture()
def site(site_config, sample_resources, sample_widgets):
    s = Site(site_config)

    # Add some sample data
    for sr in sample_resources:
        s.resources[sr.name] = sr
    for sw in sample_widgets:
        s.widgets[sw.name] = sw
    yield s


def test_import():
    assert Site.__name__ == 'Site'


def test_construction(site):
    assert site.__class__.__name__ == 'Site'


def test_add_resource_succeeds(site, sample_resource):
    site.resources[sample_resource.name] = sample_resource
    assert site.resources[sample_resource.name] == sample_resource


def test_remove_resource(site, sample_resource):
    site.resources[sample_resource.name] = sample_resource
    del site.resources[sample_resource.name]
    assert site.resources.get(sample_resource.name, None) is None


def test_section_listing(site, sample_resources):
    assert len(site.sections) == len(sample_resources) - 1


@pytest.mark.parametrize('filter_key, filter_value, expected', [
    (None, 'resource', 'About'),
    ('kbtype', 'resource', 'About'),
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
    assert results[0].title == expected


def test_filter_resources_parent(site):
    parent = DummySection('section2/index', 'Second Section')
    parent._parents = []
    child = DummyResource('section2/article2', 'Second Resource')
    child._parents = [parent]
    site.resources[parent.name] = parent
    site.resources[child.name] = child
    kw = dict(parent_name='section2/index')
    results = site.filter_resources(**kw)
    assert len(results) == 1
    assert results[0].title == 'Second Resource'


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


def test_nav_menu(site, sample_resources):
    # Only include things that want to be in the nav menu,
    # sorted by weight then by title

    navmenu_ids = [navmenu.name for navmenu in site.navmenu]
    assert navmenu_ids[0] == sample_resources[3].name
    assert navmenu_ids[1] == sample_resources[0].name
    assert navmenu_ids[2] == sample_resources[2].name
    assert navmenu_ids[3] == sample_resources[4].name


def test_remove_widget(site, sample_widget):
    site.widgets[sample_widget.name] = sample_widget
    del site.widgets[sample_widget.name]
    assert site.widgets.get(sample_widget.name, None) is None


def test_is_debug(site):
    site.config.is_debug = False
    assert not site.is_debug
    site.config.is_debug = True
    assert site.is_debug
