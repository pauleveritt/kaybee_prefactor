import os

import pytest
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture(scope='module')
def rootdir():
    return path(os.path.dirname(__file__) or '.').abspath() / 'roots'
