import pytest

from kaybee.core.events import initialize_site, purge_resources


class DummyApp:
    def __init__(self):
        self.config = dict()


class DummyEnv:
    def __init__(self, site):
        self.site = site


class Site:
    def __init__(self):
        self.resources = {}

    def remove_resource(self, name):
        del self.resources[name]


class DummyResource:
    def __init__(self, in_nav=False, weight=0):
        self.name = 'first'
        self.props = dict(
            in_nav=in_nav,
            weight=weight
        )


@pytest.fixture()
def app():
    yield DummyApp()


@pytest.fixture()
def env(site):
    yield DummyEnv(site)


@pytest.fixture()
def site(sample_resource):
    s = Site()
    s.resources[sample_resource.name] = sample_resource
    yield s


@pytest.fixture(name='sample_resource')
def dummy_resource():
    yield DummyResource()


def test_initialize_site(app, env):
    initialize_site(app, env, None)
    assert env.site.__class__.__name__ == 'Site'


def test_purge_resources(app, env, sample_resource):
    # Register the klass and add a dummy doc, make sure it's there
    assert env.site.resources.get(sample_resource.name) == sample_resource

    # Remove it, make sure it's gone
    purge_resources(None, env, sample_resource.name)
    assert env.site.resources.get(sample_resource.name) is None
