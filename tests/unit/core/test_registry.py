import dectate
import pytest

from kaybee.core.registry import (
    ResourceAction, WidgetAction, SiteAction,
    registry
)


class DummySection:
    pass


class DummySite:
    pass


@pytest.fixture()
def dummy_registry():
    class dummy_registry(dectate.App):
        dummyresource = dectate.directive(ResourceAction)
        dummywidget = dectate.directive(WidgetAction)
        dummysite = dectate.directive(SiteAction)
        add_action = registry.add_action
        first_action = registry.first_action
        get_site = registry.get_site

    yield dummy_registry


@pytest.fixture()
def register_article_no_defaults(dummy_registry):
    @dummy_registry.dummyresource('dummyarticle')
    class DummyArticle:
        pass

    yield DummyArticle


@pytest.fixture()
def register_article_defaults(dummy_registry):
    @dummy_registry.dummyresource('dummyarticle', defaults=dict(x=1),
                                  references=[1, 3])
    class DummyArticle:
        pass

    yield DummyArticle


@pytest.fixture()
def query_resource(dummy_registry):
    yield dectate.Query('dummyresource')


class TestRegistry:
    def test_construction(self, dummy_registry, register_article_no_defaults,
                          query_resource):
        dectate.commit(dummy_registry)

        results = list(query_resource(dummy_registry))
        assert len(results) == 1

    def test_clears_registray_second_time(self, dummy_registry,
                                          query_resource):
        with pytest.raises(AttributeError):
            list(query_resource(dummy_registry))

    def test_find_by_type(self, dummy_registry, register_article_no_defaults):
        dectate.commit(dummy_registry)
        da = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert da.__class__.__name__.endswith('ResourceAction')

    def test_type_defaults(self, dummy_registry, register_article_defaults):
        dectate.commit(dummy_registry)
        da = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert da.defaults['x'] == 1

    def test_type_no_defaults(self, dummy_registry,
                              register_article_no_defaults):
        dummy_registry.dummyresource('dummysection')(DummySection)
        dectate.commit(dummy_registry)
        ds = dummy_registry.first_action('dummyresource', 'dummysection')
        assert ds.defaults is None

    def test_type_references(self, dummy_registry, register_article_defaults,
                             query_resource):
        dectate.commit(dummy_registry)
        da = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert da.references == [1, 3]

    def test_type_no_references(self, dummy_registry,
                                register_article_no_defaults):
        dummy_registry.dummyresource('dummysection')(DummySection)
        dectate.commit(dummy_registry)
        da = dummy_registry.first_action('dummyresource', 'dummysection')
        assert da.references is None

    def test_imperative_add(self, dummy_registry):
        # This is how YAML-defined types will add type info
        dummy_registry.dummyresource('dummysection')(DummySection)
        dectate.commit(dummy_registry)
        assert dummy_registry.config.resources['dummysection'] == DummySection

    def test_imperative_add_defaults_references(self, dummy_registry):
        # This is how YAML-defined types will add type info
        d = dict(x=99)
        r = [1, 3]
        dummy_registry.dummyresource('dummysection',
                                     defaults=d, references=r)(DummySection)
        dectate.commit(dummy_registry)
        ds = dummy_registry.first_action('dummyresource', 'dummysection')
        assert ds.defaults['x'] == 99
        assert ds.references == [1, 3]

    def test_get_site(self, dummy_registry):
        dummy_registry.dummysite()(DummySite)
        dectate.commit(dummy_registry)
        site = dummy_registry.get_site()
        assert site.__name__.endswith('DummySite')

        # TODO
        # Test a YAML typedef getting associated with a registered class

    def test_add_action_bad_kind(self, dummy_registry):
        """ Choosing a non-existing kind should throw exception """
        dummy_registry.add_action
