"""

Integration-oriented fixtures for sphinx.testing of
generated HTML.

"""

import os

import pytest
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture(scope='module')
def rootdir():
    roots = path(os.path.dirname(__file__) or '.').abspath() / 'roots'
    return roots
