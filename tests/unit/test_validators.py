import inspect

import os
import pytest
from pykwalify.errors import SchemaError
from ruamel.yaml import load

from kaybee.core.validators import validate
from kaybee.resources.article import Article


@pytest.fixture()
def article_schema():
    fn = os.path.join(os.path.dirname(inspect.getfile(Article)),
                      'article.yaml')
    with open(fn, 'r') as f:
        return load(f)


def test_import():
    assert validate.__name__ == 'validate'


def test_validate_succeed(article_schema):
    props = dict(template='xx')
    validate(props, article_schema)


def test_validate_fail(article_schema):
    props = dict(xxxtemplate='xx')
    with pytest.raises(SchemaError):
        validate(props, article_schema)
