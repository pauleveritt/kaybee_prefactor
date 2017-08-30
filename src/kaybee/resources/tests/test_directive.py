from kaybee.resources.directives import ResourceDirective


def test_import():
    assert ResourceDirective.__name__ == 'ResourceDirective'


def test_class_defaults():
    assert ResourceDirective.has_content is True
    assert ResourceDirective.required_arguments == 1

