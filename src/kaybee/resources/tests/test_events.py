from kaybee.events import initialize_site, purge_resources
from kaybee.resources.tests.test_site import DummyResource
from kaybee.site import Site


class DummyEnv:
    pass


def test_initialize_site():
    env = DummyEnv()
    initialize_site(None, env, None)
    assert env.site.__class__.__name__ == 'Site'


def test_purge_resources():
    env = DummyEnv()
    env.site = Site()

    # Register the klass and add a dummy doc, make sure it's there
    env.site.klasses['dummyresource'] = DummyResource
    dr = DummyResource('somedoc')
    env.site.add(dr)
    assert env.site.get(dr.name).name == dr.name

    # Remove it, make sure it's gone
    purge_resources(None, env, dr.name)
    assert env.site.get(dr.name) is None