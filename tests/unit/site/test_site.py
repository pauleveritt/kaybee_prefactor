import pytest

from kaybee.core.core_type import CorePropFilterModel
from kaybee.core.site import Site
from kaybee.resources.article import Article
from kaybee.resources.category import Category
from kaybee.resources.section import Section


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
    parent = Section('section2/index', 'section', published)
    parent.title = 'Parent'
    child = Article('section2/article2', 'article', published)
    child.title = 'Child'
    site.resources[parent.name] = parent
    site.resources[child.name] = child
    kw = dict(parent_name='section2/index')
    results = site.filter_resources(**kw)
    assert len(results) == 1
    assert 'Child' == results[0].title


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


def test_is_debug(site):
    site.config.is_debug = False
    assert not site.is_debug
    site.config.is_debug = True
    assert site.is_debug


class TestReferences:
    def test_instantiation(self, site):
        assert dict() == site.references

    def test_get_reference(self, site):
        site.references['category'] = dict(cat1=99)
        target = site.get_reference('category', 'cat1')
        assert 99 == target

    def test_add_reference_target(self, site):
        # Register the shorthand "label" for a category as a reference
        cat1 = Category('section1/cat1', 'category', 'label: python')
        site.add_reference('category', 'cat1', cat1)
        target = site.get_reference('category', 'cat1')
        assert 'section1/cat1' == target.docname
