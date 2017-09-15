"""
Test the html context event handler
"""

from kaybee.events import kb_context


class DummyConfig:
    def __init__(self):
        sections = []
        kaybee_config = dict(sections=sections)
        self.html_context = dict(kaybee_config=kaybee_config)


class DummyEnv:
    def __init__(self):
        self.site = None


class DummyApp:
    def __init__(self):
        self.config = DummyConfig()
        self.env = DummyEnv()


def test_import():
    assert kb_context.__name__ == 'kb_context'

