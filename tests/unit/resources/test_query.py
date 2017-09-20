from kaybee.resources.query import Query

LOAD = 'kaybee.resources.query.Query.load'


def test_import():
    assert Query.__name__ == 'Query'


def test_instance(query, query_props):
    assert query.name == 'query1'
    assert query.props['flag'] == query_props['flag']
