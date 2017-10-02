import inspect
import os

import dectate as dectate
import pytest as pytest
from pykwalify.errors import SchemaError
from ruamel.yaml.scanner import ScannerError

from kaybee.core.decorators import ResourceAction
from kaybee.core.typedefs import KbTypedef, KbTypedefDocsError


def make_yaml_filename(fn):
    # Return a full filename relative to this directory
    current = inspect.getfile(inspect.currentframe())
    return os.path.join(
        os.path.dirname(current),
        'yaml',
        fn
    )


@pytest.fixture()
def registry():
    class DummyAction(dectate.Action):
        config = {
            'resources': dict
        }

        def __init__(self, name):
            super().__init__()
            self.name = name

        def identifier(self, resources):
            return self.name

        def perform(self, obj, resources):
            resources[self.name] = obj

    class registry(dectate.App):
        dummy = dectate.directive(DummyAction)

    yield registry


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


class TestRegistry:
    def test_construction(self, registry):
        @registry.dummy('dummyarticle')
        class DummyArticle:
            pass

        dectate.commit(registry)

        query = dectate.Query('dummy')
        results = list(query(registry))
        assert results[0][1] == 1
