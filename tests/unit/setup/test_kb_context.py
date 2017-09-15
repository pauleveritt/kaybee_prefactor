"""
Test the html context event handler
"""

from kaybee.events import kb_context


def test_import():
    assert kb_context.__name__ == 'kb_context'
