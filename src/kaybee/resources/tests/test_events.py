from kaybee.events import initialize_site, purge_resources
from kaybee.resources.tests.test_site import DummyResource
from kaybee.site import Site


class DummyConfig:
    def __init__(self):
        self.html_context = dict(
            kaybee_config=dict()
        )


class DummyApp:
    def __init__(self):
        self.config = DummyConfig()


class DummyEnv:
    pass


def test_initialize_site():
    app = DummyApp()
    env = DummyEnv()
    initialize_site(app, env, None)
    assert env.site.__class__.__name__ == 'Site'


def test_purge_resources():
    app = DummyApp()
    env = DummyEnv()
    env.site = Site(dict())

    # Register the klass and add a dummy doc, make sure it's there
    env.site.klasses['dummyresource'] = DummyResource
    dr = DummyResource('somedoc', 'Some Title')
    env.site.add(dr)
    assert env.site.get(dr.name).name == dr.name

    # Remove it, make sure it's gone
    purge_resources(None, env, dr.name)
    assert env.site.get(dr.name) is None
