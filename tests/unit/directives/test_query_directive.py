from kaybee.directives.querylist import QueryListDirective


def test_import():
    assert QueryListDirective.__name__ == 'QueryListDirective'


def test_class_defaults():
    assert QueryListDirective.has_content is True
