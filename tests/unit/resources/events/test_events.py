from kaybee.resources.events import doctree_read_resources


class TestDoctreeReadResources:
    def test_doctree_read_resources(self):
        assert 'doctree_read_resources' == doctree_read_resources.__name__

    def test_add_resource(self, mocker, app, doctree):
        doctree_read_resources(app, doctree)
        app.env.site.resources.get.assert_called_once_with('articles/a1')
