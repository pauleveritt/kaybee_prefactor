"""
Test the html context event handler
"""

from kaybee.events import kb_context


class DummyConfig:
    def __init__(self):
        sections = []
        kaybee_config = dict(sections=sections)
        self.html_context = dict(kaybee_config=kaybee_config)


class DummyApp:
    config = DummyConfig()


def test_kb_context(monkeypatch):
    monkeypatch.setattr(
        'kaybee.events.choose_layout_info',
        lambda s, p, kb: dict(style='xzy', template='pdq', active='')
    )
    app = DummyApp()
    pagename = 'firstpage'
    templatename = ''
    context = dict(meta=dict(kb_context=[]))
    doctree = None
    result = kb_context(app, pagename, templatename, context, doctree)
    assert result == 'pdq.html'
