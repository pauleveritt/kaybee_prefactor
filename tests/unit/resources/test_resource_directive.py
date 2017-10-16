import pytest

from kaybee.resources import BaseResourceDirective


class DummySite:
    added_label = None

    def __init__(self):
        self.resources = dict()

    def add_reference(self, kbtype, label, this_resource):
        self.added_label = label


class Dummy:
    pass


class SampleResource:
    def __init__(self, name, kbtype, content):
        self.name = name
        self.kbtype = kbtype
        self.content = content
        self.props = dict(template='foo')


class SampleResourceWithLabel(SampleResource):
    label = 'somelabel'


class SampleAction:
    defaults = dict()


class SampleDirective(BaseResourceDirective):
    name = 'sample_directive'


@pytest.fixture()
def dummy_directive(monkeypatch):
    monkeypatch.setattr(BaseResourceDirective, 'get_resource_class',
                        lambda x: SampleResource)
    monkeypatch.setattr(BaseResourceDirective, 'docname', 'somedocname')
    monkeypatch.setattr(BaseResourceDirective, 'site', DummySite())
    bd = SampleDirective('sample_directive', [], dict(), '', 0, 0, '', {}, {})

    yield bd


class TestBaseResourceDirective:

    def test_import(self, ):
        assert BaseResourceDirective.__name__ == 'BaseResourceDirective'

    def test_construction(self, dummy_directive):
        assert 'sample_directive' == dummy_directive.name

    def test_construction_run(self, dummy_directive):
        result = dummy_directive.run()
        assert [] == result

    def test_added_resource(self, dummy_directive):
        dummy_directive.run()
        added_resource = dummy_directive.site.resources['somedocname']
        assert 'somedocname' == added_resource.name

    def test_added_reference(self, monkeypatch):
        # This resource is a "reference", meaning it has a label.
        # Test that add_reference has the right effect.
        ds = DummySite()
        monkeypatch.setattr(BaseResourceDirective, 'get_resource_class',
                            lambda x: SampleResourceWithLabel)
        monkeypatch.setattr(BaseResourceDirective, 'docname', 'somedocname')
        monkeypatch.setattr(BaseResourceDirective, 'site', ds)
        dummy_directive2 = SampleDirective('sample_directive', [], dict(), '',
                                           0, 0, '', {},
                                           {})

        dummy_directive2.label = 'somelabel'
        dummy_directive2.run()
        assert 'somelabel' == ds.added_label
