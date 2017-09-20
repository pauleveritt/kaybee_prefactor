from kaybee.events import initialize_site, purge_resources


def test_initialize_site(app, env):
    initialize_site(app, env, None)
    assert env.site.__class__.__name__ == 'Site'


def test_purge_resources(app, env, dummy_resource):
    # Register the klass and add a dummy doc, make sure it's there
    assert env.site.get(dummy_resource.name) == dummy_resource

    # Remove it, make sure it's gone
    purge_resources(None, env, dummy_resource.name)
    assert env.site.get(dummy_resource.name) is None
