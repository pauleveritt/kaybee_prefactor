from kaybee.directives import QueryDirective


def test_import():
    assert QueryDirective.__name__ == 'QueryDirective'


def test_class_defaults():
    assert QueryDirective.has_content is True
