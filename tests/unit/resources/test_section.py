import pytest

from kaybee.resources.section import Section


@pytest.fixture()
def dummy_section():
    content = """
subheading: some subheading text
    """
    yield Section('s1', 'dummysection', content)


@pytest.fixture()
def dummy_override():
    content = """
overrides:
    article:
        template: override_article.html
    """

    yield Section('s1', 'dummysection', content)


def test_import():
    assert Section.__name__ == 'Section'


def test_construction(dummy_section):
    assert dummy_section.name == 's1'
    assert dummy_section.kbtype == 'dummysection'
    assert dummy_section.props.subheading == 'some subheading text'


def test_dummy_override(dummy_override):
    dao = dummy_override.props.overrides['article']['template']
    assert 'override_article.html' == dao
