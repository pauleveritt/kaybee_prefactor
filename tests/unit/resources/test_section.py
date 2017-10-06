import pytest

from kaybee.resources.section import Section


@pytest.fixture()
def dummy_section():
    content = """
template: somehomepage.html
subheading: some subheading text
doc_template: somesection.html
    """
    yield Section('somesection', 'dummysection', 'Some Section', content)


def test_import():
    assert Section.__name__ == 'Section'


def test_construction(dummy_section):
    assert dummy_section.name == 'somesection'
    assert dummy_section.kbtype == 'dummysection'
    assert dummy_section.title == 'Some Section'
    assert dummy_section.props.doc_template == 'somesection.html'
    assert dummy_section.props.subheading == 'some subheading text'
