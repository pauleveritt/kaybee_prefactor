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
    # site.resources.get = mocker.stub()
    app.env.site = site

    yield app


@pytest.fixture()
def doctree():
    doctree = MagicMock()
    doctree.attributes = dict(source='/foo/bar/docs/articles/a1.rst')

    yield doctree
