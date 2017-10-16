from kaybee.core.events import initialize_site, purge_resources
from kaybee.resources.events import doctree_read_resources


class TestDoctreeReadResources:
    def test_doctree_read_resources(self):
        assert 'doctree_read_resources' == doctree_read_resources.__name__

    def test_add_resource(self, mocker, app, doctree):
        doctree_read_resources(app, doctree)
        app.env.site.resources.get.assert_called_once_with('articles/a1')


def test_initialize_site(app2, env):
    initialize_site(app2, env, None)
    assert 'Site' == env.site.__class__.__name__


def test_purge_resources(app2, env, sample_resource):
    # Register the klass and add a dummy doc, make sure it's there
    assert env.site.resources.get(sample_resource.name) == sample_resource

    # Remove it, make sure it's gone
    purge_resources(None, env, sample_resource.name)
    assert env.site.resources.get(sample_resource.name) is None
