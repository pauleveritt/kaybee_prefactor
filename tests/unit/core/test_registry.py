import dectate
import pytest

from kaybee.core.registry import (
    ResourceAction, WidgetAction,
    CoreAction
)


class DummySection:
    @classmethod
    def get_schema(cls):
        return dict()


@pytest.fixture()
def dummy_registry():
    class dummy_registry(dectate.App):
        dummyresource = dectate.directive(ResourceAction)
        dummywidget = dectate.directive(WidgetAction)
        dummycore = dectate.directive(CoreAction)

    yield dummy_registry


@pytest.fixture()
def register_article(dummy_registry):
    @dummy_registry.dummyresource('dummyarticle')
    class DummyArticle:
        @classmethod
        def get_schema(cls):
            return dict()

    yield DummyArticle


@pytest.fixture()
def register_genericpage(dummy_registry):
    @dummy_registry.dummycore('dummygenericpage')
    class DummyGenericpage:
        @classmethod
        def get_schema(cls):
            return dict()

    yield DummyGenericpage


@pytest.fixture()
def query_resource(dummy_registry, register_article):
    yield dectate.Query('dummyresource')


@pytest.fixture()
def query_genericpage(dummy_registry, register_genericpage):
    yield dectate.Query('dummycore')


class TestRegistry:
    def test_construction(self, dummy_registry,
                          query_resource, query_genericpage):
        dectate.commit(dummy_registry)

        resource_results = list(query_resource(dummy_registry))
        assert 1 == len(resource_results)

        core_results = list(query_genericpage(dummy_registry))
        assert 1 == len(core_results)

    def test_clears_registry_second_time(self, dummy_registry,
                                         query_resource):
        with pytest.raises(AttributeError):
            list(query_resource(dummy_registry))
