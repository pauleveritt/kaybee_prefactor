"""
Test the html context event handler
"""
import pytest

from kaybee.core.events import (
    initialize_site, kaybee_context, purge_resources
)


class DummyResource:
    title = 'doc1 is here'

    def __init__(self):
        self.name = 'doc1'

    def parents(self, site):
        return [1, 2, 3]

    def template(self, site):
        return 'dummyresource.html'


class DummyConfig:
    kaybee_config = dict(flag=9)


class DummyEnv:
    pass


class DummySite:
    def __init__(self):
        self.resources = dict(doc1='doc1')

    def remove_resource(self, docname):
        self.resources.pop(docname, None)


class DummyApp:
    def __init__(self):
        self.config = DummyConfig()
        self.env = DummyEnv()


@pytest.fixture(name='resource')
def dummy_resource():
    yield DummyResource()


@pytest.fixture(name='app')
def dummy_app():
    yield DummyApp()


@pytest.fixture(name='env')
def dummy_env():
    yield DummyEnv()


@pytest.fixture(name='site')
def dummy_site(resource):
    ds = DummySite()
    ds.resources[resource.name] = resource
    yield ds


class TestInitializeSite:
    def test_import(self):
        assert initialize_site.__name__ == 'initialize_site'

    def test_setup(self, app, env):
        initialize_site(app, env, [])
        assert env.site.config['flag'] == 9


class TestPurgeResources:
    def test_import(self):
        assert purge_resources.__name__ == 'purge_resources'

    def test_has_site(self, app, env, site):
        env.site = site
        assert 'doc1' in env.site.resources
        purge_resources(app, env, 'doc1')
        assert 'doc1' not in env.site.resources


class TestKbContext:
    def test_import(self):
        assert kaybee_context.__name__ == 'kaybee_context'

    def test_no_resource(self, app, site):
        app.env.site = site
        docname = ''
        templatename = 'defaulttemplate'
        context = dict()
        doctree = None
        result = kaybee_context(app, docname, templatename, context, doctree)
        assert result == templatename

    def test_resource(self, app, site, resource):
        app.env.site = site
        docname = 'doc1'
        templatename = 'defaulttemplate'
        context = dict()
        doctree = None
        result = kaybee_context(app, docname, templatename, context, doctree)
        assert result == 'dummyresource.html'
        assert context['template'] == 'dummyresource.html'
        assert context['site'] == site
        assert context['resource'] == resource
        assert context['parents'] == [1, 2, 3]
        assert context['title'] == 'doc1 is here'
