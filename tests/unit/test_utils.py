import pytest

from kaybee.utils import (
    rst_to_html, get_rst_excerpt, get_rst_title,
    rst_document
)


def test_rst_document():
    source = 'Hello *world*'
    result = rst_document(source)
    assert 'document' == result.__class__.__name__


def test_rst_to_html():
    source = 'Hello *world*'
    result = rst_to_html(source)
    assert '<div class="document">' in result
    assert '<p>Hello <em>world</em></p>' in result
    assert '</div>' in result


def test_simple():
    source = """
Test *Simple*
=============

Body       
    
    """
    node = rst_document(source)
    result = get_rst_title(node)
    assert 'Test Simple' == result


@pytest.fixture()
def excerpt():
    source = """
Test
====

First *paragraph*.

Second *paragraph*.        
            """
    yield rst_document(source)


class TestGetRstExcerpt:
    def test_default(self, excerpt):
        """ By default, use the first paragraph """
        result = get_rst_excerpt(excerpt)
        assert 'First paragraph.' == result

    def test_multiple_paragraphs(self, excerpt):
        """ By configuration, you can ask for more paragraphs """

        result = get_rst_excerpt(excerpt, 2)
        assert 'First paragraph. Second paragraph.' == result

# Other excerpt policies, outside of RST extraction:
# - exclude_excerpt, on a single resource
# - exclude_excerpt site-wide
# - Getting the value from synopsis in the model
