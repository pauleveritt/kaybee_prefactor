import pytest

from kaybee.resources.article import Article


@pytest.fixture()
def dummy_article():
    content = """
    template: somearticle.html
    """
    yield Article('somearticle', 'dummyarticle', content)


def test_import(dummy_article):
    assert dummy_article.__class__.__name__ == 'Article'
