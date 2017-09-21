from kaybee.widgets.querylist import QueryList

LOAD = 'kaybee.widgets.querylist.QueryList.load'


def test_import():
    assert QueryList.__name__ == 'QueryList'


def test_instance(query):
    expected = '{"rtype": "section", "template": "query1.html"}'
    assert query.name == expected
    assert query.props['template'] == 'query1.html'
    assert query.props['rtype'] == 'section'
