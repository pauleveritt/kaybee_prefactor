from unittest.mock import MagicMock

import pytest


@pytest.fixture()
def app(mocker):
    app = MagicMock()
    app.confdir = '/foo/bar/docs'
    app.env = MagicMock()
    site = MagicMock()
    site.resources = MagicMock()
    app.test_resource = MagicMock()
    mocker.patch.object(site.resources, 'get', return_value=app.test_resource)
    app.env.site = site

    yield app


@pytest.fixture()
def doctree():
    doctree = MagicMock()
    doctree.attributes = dict(source='/foo/bar/docs/articles/a1.rst')

    yield doctree


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
def app2():
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
