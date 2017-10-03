import dectate
import pytest

from kaybee.core.registry import ResourceAction, WidgetAction, SiteAction


class DummySection:
    pass


class DummySite:
    pass


@pytest.fixture()
def registry():
    class registry(dectate.App):
        dummyresource = dectate.directive(ResourceAction)
        dummywidget = dectate.directive(WidgetAction)
        dummysite = dectate.directive(SiteAction)

        @classmethod
        def first_action(cls, kind, kbtype):
            qr = dectate.Query(kind)
            return next((x for x in qr.filter(name=kbtype)(cls)))[0]

        @classmethod
        def get_site(cls):
            """ Don't have a way to register a singleton for Dectate """
            query = dectate.Query('dummysite')
            results = list(query(registry))
            return results[0][1]

    yield registry


@pytest.fixture()
def register_article(registry):
    @registry.dummyresource('dummyarticle', defaults=dict(x=1),
                            references=[1, 3])
    class DummyArticle:
        pass

    yield DummyArticle


@pytest.fixture()
def query_resource(registry, register_article):
    yield dectate.Query('dummyresource')


class TestRegistry:
    def test_construction(self, registry, query_resource):
        dectate.commit(registry)

        results = list(query_resource(registry))
        assert len(results) == 1

    def test_clears_registray_second_time(self, registry, query_resource):
        with pytest.raises(AttributeError):
            list(query_resource(registry))

    def test_find_by_type(self, registry, query_resource):
        dectate.commit(registry)
        da = registry.first_action('dummyresource', 'dummyarticle')
        assert da.__class__.__name__.endswith('ResourceAction')

    def test_type_defaults(self, registry, query_resource):
        dectate.commit(registry)
        da = registry.first_action('dummyresource', 'dummyarticle')
        assert da.defaults['x'] == 1

    def test_type_no_defaults(self, registry):
        registry.dummyresource('dummysection')(DummySection)
        dectate.commit(registry)
        ds = registry.first_action('dummyresource', 'dummysection')
        assert ds.defaults is None

    def test_type_references(self, registry, query_resource):
        dectate.commit(registry)
        da = registry.first_action('dummyresource', 'dummyarticle')
        assert da.references == [1, 3]

    def test_type_no_references(self, registry):
        registry.dummyresource('dummysection')(DummySection)
        dectate.commit(registry)
        da = registry.first_action('dummyresource', 'dummysection')
        assert da.references is None

    def test_imperative_add(self, registry):
        # This is how YAML-defined types will add type info
        registry.dummyresource('dummysection')(DummySection)
        dectate.commit(registry)
        assert registry.config.resources['dummysection'] == DummySection

    def test_imperative_add_defaults_references(self, registry):
        # This is how YAML-defined types will add type info
        d = dict(x=99)
        r = [1, 3]
        registry.dummyresource('dummysection',
                               defaults=d, references=r)(DummySection)
        dectate.commit(registry)
        ds = registry.first_action('dummyresource', 'dummysection')
        assert ds.defaults['x'] == 99
        assert ds.references == [1, 3]

    def test_get_site(self, registry):
        registry.dummysite()(DummySite)
        dectate.commit(registry)
        site = registry.get_site()

        # TODO
        # Test a YAML typedef getting associated with a registered class
        # Unwind the fixtures in here, be more manual/explicit
        # Move over the class method from decorator and write tests
