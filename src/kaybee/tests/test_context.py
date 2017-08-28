"""
Test the html context event handler
"""

import pytest
from kaybee import kb_context


class DummyConfig:
    def __init__(self):
        global_navigation = []
        kaybee_config = dict(global_navigation=global_navigation)
        self.html_context = dict(kaybee_config=kaybee_config)


class DummyApp:
    config = DummyConfig()


def test_kb_context(monkeypatch):
    monkeypatch.setattr(
        'kaybee.choose_layout_info',
        lambda s, p, kb: dict(style='xzy', template='pdq')
    )
    app = DummyApp()
    pagename = 'firstpage'
    templatename = ''
    context = dict(meta=dict(kb_context=[]))
    doctree = None
    result = kb_context(app, pagename, templatename, context, doctree)
    assert result == 'pdq.html'
