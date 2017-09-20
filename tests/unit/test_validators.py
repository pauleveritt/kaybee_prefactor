import pytest
from pykwalify.errors import SchemaError, CoreError


def test_import(Validator):
    assert Validator.__name__ == 'Validator'


def test_defaultschema_validate_succeed(validator, dummy_resource):
    validator.validate(dummy_resource)


def test_defaultschema_validate_fail(validator, dummy_resource):
    dummy_resource.props['xxx'] = 'xxx'
    with pytest.raises(SchemaError):
        validator.validate(dummy_resource)


def test_customschema_validate_fail(validator, dummy_resource):
    dummy_resource.schema_filename = '/Fake/Path'
    with pytest.raises(CoreError):
        validator.validate(dummy_resource)
