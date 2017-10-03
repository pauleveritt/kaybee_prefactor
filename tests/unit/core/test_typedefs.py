import inspect
import os

import pytest
from pykwalify.errors import SchemaError
from ruamel.yaml.scanner import ScannerError

from kaybee.core.typedefs import YamlTypedef, KbTypedefDocsError

YAMLTYPEDEF_PATH = 'kaybee.core.typedefs.YamlTypedef'
LOAD = YAMLTYPEDEF_PATH + '.load'
READ = YAMLTYPEDEF_PATH + '.read'
VALIDATE = YAMLTYPEDEF_PATH + '.validate'
skip = lambda x: None


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
            yaml_typedef = YamlTypedef(yaml_fn)

    def test_exception_not_two_docs(self, monkeypatch):
        yaml_fn = make_yaml_filename('not_two_docs.yaml')
        with pytest.raises(KbTypedefDocsError):
            yaml_typedef = YamlTypedef(yaml_fn)

    def test_exception_not_valid_typedef(self, monkeypatch):
        yaml_fn = make_yaml_filename('not_valid_article.yaml')
        with pytest.raises(SchemaError):
            YamlTypedef(yaml_fn=yaml_fn)
            yaml_typedef = YamlTypedef(yaml_fn)
