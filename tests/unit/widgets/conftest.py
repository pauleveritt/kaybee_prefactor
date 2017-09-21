import pytest

from kaybee.widgets import BaseWidget
from kaybee.widgets.query import Query


@pytest.fixture(name='base_widget')
def dummy_base_widget():
    content = """
template: widget1.html
rtype: section    
    """
    yield BaseWidget(content)


@pytest.fixture(name='query')
def dummy_query():
    content = """
template: query1.html
rtype: section    
    """
    yield Query(content)
