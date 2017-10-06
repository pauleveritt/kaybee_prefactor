import pytest

from kaybee.resources import BaseDirective


class DummySite:
    def add_resource(self, resource):
        self.resource = resource


class Dummy:
    pass


class SampleResource:
    def __init__(self, *args, **kw):
        self.props = dict(template='foo')


class SampleAction:
    defaults = dict()


class SampleDirective(BaseDirective):
    name = 'sample_directive'


@pytest.fixture(name='base_directive')
def dummy_directive():
    bd = SampleDirective('', [], dict(), '', 0, 0, '', {}, {})
    bd.state = Dummy()
    bd.state.document = Dummy()
    bd.state.document.settings = Dummy()
    bd.state.document.settings.env = Dummy()
    bd.state.document.settings.env.site = DummySite()
    bd.state.document.settings.env.site.validator = Dummy()

    bd.state.document.settings.env.site.validator.validate = lambda x: True
    bd.state.document.settings.env.docname = 'xyz'
    bd.state.parent = Dummy()
    bd.state.parent.parent = Dummy()
    bd.config = Dummy()

    yield bd


def test_import():
    assert BaseDirective.__name__ == 'BaseDirective'


def test_construction(base_directive):
    assert base_directive.run


def test_construction_run(monkeypatch, base_directive):
    monkeypatch.setattr(BaseDirective, 'get_resource_class',
                        lambda x: SampleResource)
    monkeypatch.setattr(BaseDirective, 'doc_title',
                        lambda x: 'Some Title')
    result = base_directive.run()
    assert result == []
