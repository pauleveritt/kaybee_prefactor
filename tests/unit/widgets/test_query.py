from kaybee.widgets.query import Query

LOAD = 'kaybee.widgets.query.Query.load'


def test_import():
    assert Query.__name__ == 'Query'


def test_instance(query):
    expected = '{"rtype": "section", "template": "query1.html"}'
    assert query.name == expected
    assert query.props['template'] == 'query1.html'
    assert query.props['rtype'] == 'section'
