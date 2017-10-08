import pytest

from kaybee.resources.category import Category


@pytest.fixture()
def dummy_article():
    content = """
label: category1
    """
    yield Category('somecategory', 'category', 'C1', content)

