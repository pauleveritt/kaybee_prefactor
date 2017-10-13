import pytest

from kaybee.widgets.querylist import QueryList


class DummySite:
    def filter_resources(self, **kw):
        return []


@pytest.fixture()
def dummy_querylist():
    content = """
    template: querylist.html
    queries:
        - label: Recent Blog Posts
          style: primary
          query:
              kbtype: section
              limit: 5
    """
    yield QueryList('somewidget', 'dummywidget', content)


@pytest.fixture()
def dummy_site():
    yield DummySite()


def test_import(dummy_querylist):
    assert dummy_querylist.__class__.__name__


def test_construction(dummy_querylist):
    dp = dummy_querylist.props
    assert dp.template == 'querylist.html'
    assert len(dp.queries) == 1
    dp0 = dp.queries[0]
    assert dp0.label == 'Recent Blog Posts'
    assert dp0.style == 'primary'
    assert dp0.query.kbtype == 'section'
    assert dp0.query.limit == 5


def test_make_context(dummy_querylist, dummy_site):
    context = dict()
    dummy_querylist.make_context(context, dummy_site)
    expected = [dict(
        label='Recent Blog Posts',
        results=[],
        style='primary'
    )]
    assert context['result_sets'] == expected
