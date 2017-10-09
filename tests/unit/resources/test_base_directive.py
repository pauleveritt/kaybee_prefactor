import pytest

from kaybee.resources import BaseResourceDirective


class DummySite:
    def __init__(self):
        self.resources = dict()


class Dummy:
    pass


class SampleResource:
    def __init__(self, *args, **kw):
        self.name = 'name'
        self.props = dict(template='foo')


class SampleAction:
    defaults = dict()


class SampleDirective(BaseResourceDirective):
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
    assert BaseResourceDirective.__name__ == 'BaseResourceDirective'


def test_construction(base_directive):
    assert base_directive.run


def test_construction_run(monkeypatch, base_directive):
    monkeypatch.setattr(BaseResourceDirective, 'get_resource_class',
                        lambda x: SampleResource)
    monkeypatch.setattr(BaseResourceDirective, 'doc_title',
                        lambda x: 'Some Title')
    result = base_directive.run()
    assert result == []
