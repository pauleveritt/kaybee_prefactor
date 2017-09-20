import pytest
from pykwalify.errors import SchemaError, CoreError


def test_import(Validators):
    assert Validators.__name__ == 'Validators'


def test_defaultschema_validate_succeed(validators, dummy_resource):
    validators.validate(dummy_resource)


def test_defaultschema_validate_fail(validators, dummy_resource):
    dummy_resource.props['xxx'] = 'xxx'
    with pytest.raises(SchemaError):
        validators.validate(dummy_resource)


def test_customschema_validate_fail(validators, dummy_resource):
    dummy_resource.schema_filename = '/Fake/Path'
    with pytest.raises(CoreError):
        validators.validate(dummy_resource)
