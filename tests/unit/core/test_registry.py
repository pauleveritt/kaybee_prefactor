import dectate
import pytest

from kaybee.core.registry import (
    ResourceAction, WidgetAction, SiteAction,
    KbActionInvalidKind
)


class DummySection:
    @classmethod
    def get_schema(cls):
        return dict()


class DummySite:
    pass


@pytest.fixture()
def dummy_registry():
    class dummy_registry(dectate.App):
        dummyresource = dectate.directive(ResourceAction)
        dummywidget = dectate.directive(WidgetAction)
        dummysite = dectate.directive(SiteAction)

        @classmethod
        def add_action(cls, kind, kbtype, klass, defaults=None,
                       references=None):
            """ YAML types imperatively add config per contract """

            # Get the kind, raise custom exception if it doesn't exist
            k = getattr(cls, kind, None)
            if k is None:
                raise KbActionInvalidKind(kind)

            k(kbtype, defaults=defaults, references=references)(klass)

        @classmethod
        def first_action(cls, kind, kbtype):
            """ Get type config info from the kbtype of certain kind """
            qr = dectate.Query(kind)
            # Use a generator expression to get the first action
            # in "kind" with a name of ktype. kind might be
            # "resource" or "widget", kbtype might be "article".
            return next((x for x in qr.filter(name=kbtype)(cls)))[0]

        @classmethod
        def get_class(cls, kind, kbtype):
            q = dectate.Query(kind)
            klass = [i[1] for i in list(q(cls)) if i[0].name == kbtype][0]
            return klass

        @classmethod
        def get_site(cls, sitename='site'):
            """ Don't have a way to register a singleton for Dectate """
            query = dectate.Query(sitename)
            results = list(query(cls))
            return results[0][1]

    yield dummy_registry


@pytest.fixture()
def register_article_no_defaults(dummy_registry):
    @dummy_registry.dummyresource('dummyarticle')
    class DummyArticle:
        @classmethod
        def get_schema(cls):
            return dict()

    yield DummyArticle


@pytest.fixture()
def register_article_defaults(dummy_registry):
    @dummy_registry.dummyresource('dummyarticle', defaults=dict(x=1),
                                  references=[1, 3])
    class DummyArticle:
        @classmethod
        def get_schema(cls):
            return dict()

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

    def test_clears_registry_second_time(self, dummy_registry,
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
        dectate.commit(dummy_registry)
        ds = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert ds.defaults is None

    def test_type_references(self, dummy_registry, register_article_defaults,
                             query_resource):
        dectate.commit(dummy_registry)
        da = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert da.references == [1, 3]

    def test_type_no_references(self, dummy_registry,
                                register_article_no_defaults):
        dectate.commit(dummy_registry)
        da = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert da.references is None

    def test_imperative_add(self, dummy_registry):
        # This is how YAML-defined types will add type info
        dummy_registry.add_action('dummyresource', 'dummysection',
                                  DummySection)
        dectate.commit(dummy_registry)
        assert dummy_registry.config.resources['dummysection'] == DummySection

    def test_imperative_add_defaults_references(self, dummy_registry):
        # This is how YAML-defined types will add type info
        d = dict(x=99)
        r = [1, 3]
        dummy_registry.add_action(
            'dummyresource', 'dummysection', DummySection,
            defaults=d, references=r)
        dectate.commit(dummy_registry)
        ds = dummy_registry.first_action('dummyresource', 'dummysection')
        assert ds.defaults['x'] == d['x']
        assert ds.references == r

    def test_get_class(self, dummy_registry, register_article_no_defaults):
        dectate.commit(dummy_registry)
        klass = dummy_registry.get_class('dummyresource', 'dummyarticle')
        assert klass.__name__.endswith('DummyArticle')

    def test_get_site(self, dummy_registry):
        dummy_registry.dummysite()(DummySite)
        dectate.commit(dummy_registry)
        site = dummy_registry.get_site('dummysite')
        assert site.__name__.endswith('DummySite')

    def test_add_action_bad_kind(self, dummy_registry):
        """ Choosing a non-existing kind should throw exception """

        with pytest.raises(KbActionInvalidKind) as excinfo:
            dummy_registry.add_action = dummy_registry.add_action(
                'xxxresource', 'dummysection', DummySection
            )
        assert 'xxxresource' in str(excinfo.value)
