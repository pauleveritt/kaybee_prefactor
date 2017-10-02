import inspect
import os

import dectate as dectate
import pytest as pytest
from pykwalify.errors import SchemaError
from ruamel.yaml.scanner import ScannerError

from kaybee.core.typedefs import KbTypedef, KbTypedefDocsError


def make_yaml_filename(fn):
    # Return a full filename relative to this directory
    current = inspect.getfile(inspect.currentframe())
    return os.path.join(
        os.path.dirname(current),
        'yaml',
        fn
    )


class TestKbTypedf:
    def test_import(self):
        assert KbTypedef.__name__ == 'KbTypedef'

    def test_exception_not_well_formed(self):
        yaml_fn = make_yaml_filename('not_well_formed_article.yaml')
        with pytest.raises(ScannerError):
            KbTypedef(yaml_fn=yaml_fn)

    def test_exception_not_two_docs(self):
        yaml_fn = make_yaml_filename('not_two_docs.yaml')
        with pytest.raises(KbTypedefDocsError):
            KbTypedef(yaml_fn=yaml_fn)

    def test_exception_not_valid_typedef(self):
        yaml_fn = make_yaml_filename('not_valid_article.yaml')
        with pytest.raises(SchemaError):
            KbTypedef(yaml_fn=yaml_fn)


class DummySection:
    pass


@pytest.fixture()
def registry():
    class DummyResourceAction(dectate.Action):
        config = {
            'resources': dict
        }

        def __init__(self, name, defaults=None, references=None):
            super().__init__()
            self.name = name
            self.defaults = defaults
            self.references = references

        def identifier(self, resources):
            return self.name

        def perform(self, obj, resources):
            resources[self.name] = obj

    class DummyWidgetAction(dectate.Action):
        config = {
            'widgets': dict
        }

        def __init__(self, name, defaults=None, references=None):
            super().__init__()
            self.name = name
            self.defaults = defaults
            self.references = references

        def identifier(self, widgets):
            return self.name

        def perform(self, obj, widgets):
            widgets[self.name] = obj

    class registry(dectate.App):
        dummyresource = dectate.directive(DummyResourceAction)
        dummywidget = dectate.directive(DummyWidgetAction)

        @classmethod
        def first_action(cls, kind, kbtype):
            qr = dectate.Query(kind)
            return next((x for x in qr.filter(name=kbtype)(cls)))[0]

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
        assert da.__class__.__name__.endswith('DummyResourceAction')

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
