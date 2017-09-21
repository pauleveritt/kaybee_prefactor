import pytest

from kaybee.site import Site


def test_import():
    assert Site.__name__ == 'Site'


def test_construction(site):
    assert site.__class__.__name__ == 'Site'


def test_get_class_succeeds(site, dummy_resource):
    drc = dummy_resource.__class__
    assert site.get_class(drc.__name__.lower()) == drc


def test_get_class_fails(site):
    with pytest.raises(KeyError):
        site.get_class('xx')


def test_add_resource_succeeds(site, dummy_resource):
    site.add_resource(dummy_resource)
    assert site.resources.get(dummy_resource.name) == dummy_resource


def test_add_resource_fails(site, dummy_resource):
    # Remove the registered class first
    del site.klasses['dummyresource']
    with pytest.raises(AssertionError):
        site.add_resource(dummy_resource)


def test_remove_resource(site, dummy_resource):
    site.add_resource(dummy_resource)
    site.remove_resource(dummy_resource.name)
    assert site.resources.get(dummy_resource.name, None) is None


def test_section_listing(site, SAMPLE_RESOURCES):
    assert len(site.sections) == len(SAMPLE_RESOURCES) - 1


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


def test_nav_menu(site, SAMPLE_RESOURCES):
    # Only include things that want to be in the nav menu,
    # sorted by weight then by title

    navmenu_ids = [navmenu.name for navmenu in site.navmenu]
    assert navmenu_ids[0] == SAMPLE_RESOURCES[3].name
    assert navmenu_ids[1] == SAMPLE_RESOURCES[0].name
    assert navmenu_ids[2] == SAMPLE_RESOURCES[2].name
    assert navmenu_ids[3] == SAMPLE_RESOURCES[4].name


def test_validator_exists(site):
    assert site.validator.__class__.__name__ == 'Validator'
