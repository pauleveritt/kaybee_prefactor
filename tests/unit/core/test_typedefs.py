import inspect
import os

import dectate
import pytest
from pykwalify.errors import SchemaError
from ruamel.yaml.scanner import ScannerError

from kaybee.core.registry import registry, ResourceAction
from kaybee.core.typedefs import (
    YamlTypedef, KbTypedefDocsError,
    KbTypedefInvalidDefault,
    KbTypedefReference,
    KbTypedefInvalidClass
)

YAMLTYPEDEF_PATH = 'kaybee.core.typedefs.YamlTypedef'
LOAD = YAMLTYPEDEF_PATH + '.load'
READ = YAMLTYPEDEF_PATH + '.read'
VALIDATE = YAMLTYPEDEF_PATH + '.validate'


def skip(self):
    return None


def make_yaml_filename(fn):
    # Return a full filename relative to this directory
    current = inspect.getfile(inspect.currentframe())
    return os.path.join(
        os.path.dirname(current),
        'yaml',
        fn
    )


class TestYamlTypedf:
    def test_import(self):
        assert YamlTypedef.__name__ == 'YamlTypedef'

    def test_construction(self, monkeypatch):
        monkeypatch.setattr(LOAD, skip)
        monkeypatch.setattr(READ, skip)
        monkeypatch.setattr(VALIDATE, skip)
        fn = make_yaml_filename('valid_article.yaml')
        yaml_typedef = YamlTypedef(fn)

        assert yaml_typedef.__class__.__name__ == 'YamlTypedef'
        assert yaml_typedef.yaml_fn.endswith('valid_article.yaml')
        assert yaml_typedef.yaml_content is None
        assert yaml_typedef.typeinfo is None
        assert yaml_typedef.schema is None

    def test_read(self, monkeypatch):
        monkeypatch.setattr(VALIDATE, skip)
        fn = make_yaml_filename('valid_article.yaml')
        yaml_typedef = YamlTypedef(fn)
        header = '# Well-formed AND valid YAML'
        assert yaml_typedef.yaml_content.startswith(header)

    def test_load_successfully(self, monkeypatch):
        monkeypatch.setattr(VALIDATE, skip)
        fn = make_yaml_filename('valid_article.yaml')
        yaml_typedef = YamlTypedef(fn)
        assert len(yaml_typedef.typeinfo.keys())
        assert len(yaml_typedef.schema.keys())

    def test_exception_not_well_formed(self, monkeypatch):
        yaml_fn = make_yaml_filename('not_well_formed_article.yaml')
        with pytest.raises(ScannerError):
            YamlTypedef(yaml_fn)

    def test_exception_not_two_docs(self, monkeypatch):
        yaml_fn = make_yaml_filename('not_two_docs.yaml')
        with pytest.raises(KbTypedefDocsError):
            YamlTypedef(yaml_fn)

    def test_exception_not_valid_typedef(self, monkeypatch):
        yaml_fn = make_yaml_filename('not_valid_article.yaml')
        with pytest.raises(SchemaError):
            YamlTypedef(yaml_fn=yaml_fn)
            YamlTypedef(yaml_fn)

    def test_valid_yaml(self):
        yaml_fn = make_yaml_filename('valid_article.yaml')
        YamlTypedef(yaml_fn)

    def test_valid_properties_core(self):
        yaml_fn = make_yaml_filename('valid_article.yaml')
        yaml_typedef = YamlTypedef(yaml_fn)
        assert yaml_typedef.kind == 'resource'
        assert yaml_typedef.kbtype == 'dummyarticle'
        assert yaml_typedef.based_on == 'section'
        assert yaml_typedef.defaults == dict()
        assert yaml_typedef.references == []

    def test_bad_kbtype(self):
        yaml_fn = make_yaml_filename('article_bad_kbtype.yaml')
        with pytest.raises(SchemaError):
            YamlTypedef(yaml_fn)

    def test_valid_properties_defaults_references(self):
        yaml_fn = make_yaml_filename('valid_article_defaults_references.yaml')
        yaml_typedef = YamlTypedef(yaml_fn)
        assert yaml_typedef.defaults['style'] == 'defaultstyle'
        assert yaml_typedef.references[0] == 'author'

    def test_bad_defaults(self):
        yaml_fn = make_yaml_filename('bad_article_defaults.yaml')
        with pytest.raises(KbTypedefInvalidDefault) as exc:
            YamlTypedef(yaml_fn)
        assert 'xxxstyle' in str(exc.value)

    def test_bad_references(self):
        yaml_fn = make_yaml_filename('bad_article_references.yaml')
        with pytest.raises(KbTypedefReference) as exc:
            YamlTypedef(yaml_fn)
        assert 'xxxauthor' in str(exc.value)


@pytest.fixture()
def dummy_registry():
    class dummy_registry(registry):
        dummyresource = dectate.directive(ResourceAction)

    dummy_registry.add_action('dummyresource', 'dummysection',
                              DummySection)
    dectate.commit(dummy_registry)

    yield dummy_registry


class DummySection:
    pass


@pytest.fixture()
def query_resource(dummy_registry):
    yield dectate.Query('dummyresource')


class TestIntegration:
    """ Hook up to the registry for testing """

    def test_good_add(self, dummy_registry):
        """ Create new type and add to registry """
        yaml_fn = make_yaml_filename('valid_article_defaults_references.yaml')
        yaml_typedef = YamlTypedef(yaml_fn)
        yaml_typedef.register(dummy_registry)
        # kind = yaml_typedef.kind
        # kbtype = yaml_typedef.kbtype
        # defaults = yaml_typedef.defaults
        # references = yaml_typedef.references
        # dummy_registry.add_action(
        #     kind, kbtype, DummySection,
        #     defaults=defaults, references=references,
        # )
        dectate.commit(dummy_registry)
        assert dummy_registry.config.resources['dummyarticle'] == DummySection
        da = dummy_registry.first_action('dummyresource', 'dummyarticle')
        assert da.defaults['style'] == 'defaultstyle'

    def test_bad_based_on(self, dummy_registry):
        """ YAML typedef pointed to an unregistered action """
        yaml_fn = make_yaml_filename('bad_article_based_on.yaml')
        yaml_typedef = YamlTypedef(yaml_fn)
        with pytest.raises(KbTypedefInvalidClass) as exc:
            yaml_typedef.get_class(dummy_registry)
        assert 'based_on: xxxdummysection' in str(exc.value)

# TODO Other tests:
# - label triggers the creation of a reference
# - references points to an author that doesn't exist
