"""

Integration-oriented fixtures for sphinx.testing of
generated HTML.

"""

import os

import pytest
from bs4 import BeautifulSoup
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture(scope='module')
def rootdir():
    roots = path(os.path.dirname(__file__) or '.').abspath() / 'roots'
    return roots


@pytest.fixture()
def content(app):
    app.build()
    yield app


@pytest.fixture()
def pages(content, request):
    all_pages = {}
    for pn in request.module.pagepaths:
        c = (content.outdir / pn).text()
        all_pages[pn] = BeautifulSoup(c, 'html5lib')
    yield all_pages
