import pytest

from kaybee.widgets.sectionquery import SectionQuery


class DummySite:
    def filter_resources(self, **kw):
        return []


@pytest.fixture(name='sectionquery')
def dummy_sectionquery():
    content = """
    template: sectionquery.html
    queries:
        - label: Recent Blog Posts
          style: primary
          rtype: section
          limit: 5
    """
    yield SectionQuery(content)


@pytest.fixture(name='sample_site')
def dummy_site():
    yield DummySite()


def test_import(sectionquery):
    assert sectionquery.__class__.__name__


def test_make_context(sectionquery, sample_site):
    context = dict()
    mc = sectionquery.make_context(context, sample_site)
    results = []
    assert context['result_count'] == 0
    assert context['results'] == results