import pytest

from kaybee.widgets.querylist import QueryList


class DummySite:
    def filter_resources(self, **kw):
        return []


@pytest.fixture(name='querylist')
def dummy_querylist():
    content = """
    template: querylist.html
    queries:
        - label: Recent Blog Posts
          style: primary
          rtype: section
          limit: 5
    """
    yield QueryList(content)


@pytest.fixture(name='sample_site')
def dummy_site():
    yield DummySite()


def test_import(querylist):
    assert querylist.__class__.__name__


def test_make_context(querylist, sample_site):
    context = dict()
    mc = querylist.make_context(context, sample_site)
    expected = [dict(
        label='Recent Blog Posts',
        results=[],
        style='primary'
    )]
    assert context['result_sets'] == expected
