import pytest
from pykwalify.errors import SchemaError, CoreError


class DummyResource:
    def __init__(self, in_nav=False, weight=0):
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )


@pytest.fixture()
def Validator():
    from kaybee.core.validators import Validator
    yield Validator


@pytest.fixture()
def validator(Validator):
    yield Validator()


@pytest.fixture()
def dummy_resource():
    yield DummyResource()


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
