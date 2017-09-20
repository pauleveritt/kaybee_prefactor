import pytest


class DummyResource:
    def __init__(self, rtype='dummyresource', props=None):
        self.rtype = rtype
        if props is None:
            self.props = dict()
        else:
            self.props = props


@pytest.fixture()
def dummy_resource():
    yield DummyResource()


@pytest.fixture()
def Validators():
    from kaybee.validators import Validators
    yield Validators


@pytest.fixture()
def validators(Validators):
    yield Validators()


@pytest.fixture()
def sample_yaml():
    return """
name: Sample Yaml
age: 99    
    """


@pytest.fixture()
def sample_props():
    return dict(name='Sample Yaml', age=99)
