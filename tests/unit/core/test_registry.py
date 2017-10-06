import dectate
import pytest

from kaybee.core.registry import (
    ResourceAction, WidgetAction
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
def query_resource(dummy_registry):
    yield dectate.Query('dummyresource')


class TestRegistry:
    def test_construction(self, dummy_registry, register_article,
                          query_resource):
        dectate.commit(dummy_registry)

        results = list(query_resource(dummy_registry))
        assert len(results) == 1

    def test_clears_registry_second_time(self, dummy_registry,
                                         query_resource):
        with pytest.raises(AttributeError):
            list(query_resource(dummy_registry))
