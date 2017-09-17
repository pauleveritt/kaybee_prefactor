from kaybee.directives import QueryDirective, query

LOAD = 'kaybee.directives.QueryDirective.load'


def test_qd_import():
    assert QueryDirective.__name__ == 'QueryDirective'


def test_qn_import():
    assert query.__name__ == 'QueryNode'


def test_qn_construction():
    qn = query()
    assert qn.__class__.__name__ == 'QueryNode'


def test_qd_class_defaults():
    assert QueryDirective.has_content is True


def test_qd_yaml_load_empty():
    content = """
    
    
    """
    props = QueryDirective.load(content)
    assert props == dict()


def test_qd_package_dir():
    assert QueryDirective.package_dir().endswith('kaybee/directives')


def test_qd_yaml_load():
    content = """
flag1: 1    
flag2: 2    
    """
    props = QueryDirective.load(content)
    assert props == dict(flag1=1, flag2=2)

#
# Giving up at this point, contructing a Directive is
# quite painful. Switch to integration tests.
#