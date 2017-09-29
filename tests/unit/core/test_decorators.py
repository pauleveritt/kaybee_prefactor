import pytest

from kaybee.core.decorators import SiteAction, ResourceAction, WidgetAction, kb


class DummySite:
    pass


class DummyResource:
    def __init__(self):
        self.rtype = None

    @classmethod
    def set_rtype(cls, rtype):
        cls.rtype = rtype


class DummyWidget:
    def __init__(self):
        self.wtype = None

    @classmethod
    def set_wtype(cls, wtype):
        cls.wtype = wtype


@pytest.fixture(name='site')
def dummy_site():
    yield dict()


class TestSiteAction:
    def test_import(self):
        assert SiteAction.__name__ == 'SiteAction'

    def test_constructor(self):
        action = SiteAction()
        assert action.name == 'singleton'

    def test_identifier(self, site):
        action = SiteAction()
        assert action.identifier(site) == 'singleton'

    def test_perform(self, site):
        action = SiteAction()
        action.perform(DummySite, site)
        assert site['singleton'] == DummySite


class TestResourceAction:
    def test_import(self):
        assert ResourceAction.__name__ == 'ResourceAction'

    def test_constructor(self):
        action = ResourceAction('ra')
        assert action.name == 'ra'

    def test_identifier(self, site):
        action = ResourceAction('ra')
        assert action.identifier(site) == 'ra'

    def test_perform(self, site):
        action = ResourceAction('ra')
        action.perform(DummyResource, site)
        assert site['ra'] == DummyResource


class TestWidgetAction:
    def test_import(self):
        assert WidgetAction.__name__ == 'WidgetAction'

    def test_constructor(self):
        action = WidgetAction('wa')
        assert action.name == 'wa'

    def test_identifier(self, site):
        action = WidgetAction('wa')
        assert action.identifier(site) == 'wa'

    def test_perform(self, site):
        action = WidgetAction('wa')
        action.perform(DummyWidget, site)
        assert site['wa'] == DummyWidget


class TestKb:
    def test_import(self):
        assert kb.__name__ == 'kb'
        assert kb.widget.__name__ == 'method'
        assert kb.resource.__name__ == 'method'
        assert kb.site.__name__ == 'method'
        assert kb.get_site.__name__ == 'get_site'