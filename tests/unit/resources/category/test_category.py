import pytest
from pydantic.exceptions import ValidationError

from kaybee.resources.category import Category


def test_import(dummy_article):
    assert dummy_article.__class__.__name__ == 'Category'


def test_construction_success(dummy_article):
    assert 'category1' == dummy_article.props.label


def test_invalid_yaml():
    with pytest.raises(ValidationError):
        Category('somecategory', 'category', 'c2', '')
