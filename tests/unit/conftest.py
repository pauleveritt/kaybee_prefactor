import pytest

from kaybee.site import Site


class DummyConfig:
    def __init__(self):
        self.html_context = dict(
            kaybee_config=dict()
        )


class DummyApp:
    def __init__(self, config):
        self.config = config


class DummyEnv:
    def __init__(self, site):
        self.site = site


class DummySection:
    rtype = 'section'

    def __init__(self, name, title,
                 in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )

    def __str__(self):
        return self.name


class DummyResource:
    rtype = 'resource'

    def __init__(self, name, title, in_nav=False, weight=0):
        self.name = name
        self.title = title
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )


@pytest.fixture(name='SAMPLE_RESOURCES')
def sample_resources():
    yield (
        DummySection('8783', 'The First', in_nav=True),
        DummySection('1343', 'Second should sort ahead of first'),
        DummySection('4675', 'Z Last weights first', in_nav=True),
        DummySection('9856', 'Q Not Last No Weight', in_nav=True, weight=-10),
        DummyResource('4444', 'About', in_nav=True, weight=20)
    )


@pytest.fixture()
def dummy_resource(SAMPLE_RESOURCES):
    yield SAMPLE_RESOURCES[4]


@pytest.fixture()
def Validator():
    from kaybee.validators import Validator
    yield Validator


@pytest.fixture()
def validator(Validator):
    yield Validator()


@pytest.fixture()
def sample_yaml():
    return """
name: Sample Yaml
age: 99    
    """


@pytest.fixture()
def sample_props():
    return dict(name='Sample Yaml', age=99)


@pytest.fixture()
def site_config():
    yield dict()


@pytest.fixture()
def site(site_config, SAMPLE_RESOURCES):
    s = Site(site_config)

    # Register classes
    s.klasses['dummyresource'] = DummyResource
    s.klasses['dummysection'] = DummySection

    # Add some sample data
    [s.add(i) for i in SAMPLE_RESOURCES]
    yield s


@pytest.fixture()
def config():
    yield DummyConfig()


@pytest.fixture()
def app(config):
    yield DummyApp(config)


@pytest.fixture()
def env(site):
    yield DummyEnv(site)
