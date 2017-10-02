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
