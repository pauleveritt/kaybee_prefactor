"""
Test the html context event handler
"""

from kaybee.events import kb_context
from kaybee.site import Site

FIRSTPAGE = 'firstpage'


class DummyResource:
    template = 'dummyresourcetemplate'

    def __init__(self, name):
        self.name = name

    def parents(self, site):
        return []


class DummyConfig:
    def __init__(self):
        sections = []
        kaybee_config = dict(sections=sections)
        self.html_context = dict(kaybee_config=kaybee_config)


class DummyEnv:
    def __init__(self):
        self.site = Site()
        self.site.klasses['dummyresource'] = DummyResource
        dr = DummyResource(FIRSTPAGE)
        self.site.add(dr)


class DummyApp:
    def __init__(self):
        self.config = DummyConfig()
        self.env = DummyEnv()


def test_import():
    assert kb_context.__name__ == 'kb_context'

def test_context_get_site():
    pass


# def test_kb_context(monkeypatch):
#     monkeypatch.setattr(
#         'kaybee.events.choose_layout_info',
#         lambda s, p, kb: dict(style='xzy', template='pdq', active='')
#     )
#     app = DummyApp()
#     pagename = FIRSTPAGE
#     templatename = ''
#     context = dict(meta=dict(kb_context=[]))
#     doctree = None
#     result = kb_context(app, pagename, templatename, context, doctree)
#     assert result == DummyResource.template + '.html'
