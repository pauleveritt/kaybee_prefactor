from kaybee.directives.querylist import QueryListDirective, querylist


def test_import_node():
    assert querylist.__name__ == 'querylist'


def test_import_directive():
    assert QueryListDirective.__name__ == 'QueryListDirective'


def test_class_defaults():
    assert QueryListDirective.has_content is True
