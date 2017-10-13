import pytest

from kaybee.resources.homepage import Homepage


@pytest.fixture()
def dummy_homepage():
    content = """
template: somehomepage.html
logo: somelogo.png
    """
    yield Homepage('somehomepage', 'dummyhomepage', content)


def test_import(dummy_homepage):
    assert dummy_homepage.__class__.__name__ == 'Homepage'


def test_construction(dummy_homepage):
    assert dummy_homepage.props.template == 'somehomepage.html'
    assert dummy_homepage.props.logo == 'somelogo.png'
