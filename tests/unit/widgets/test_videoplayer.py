import pytest

from kaybee.widgets.videoplayer import VideoPlayer


@pytest.fixture()
def dummy_videoplayer():
    content = """
src: http://foo.com/x
    """
    yield VideoPlayer('somewidget', 'dummywidget', content)


def test_import():
    assert VideoPlayer.__name__ == 'VideoPlayer'


def test_construction(dummy_videoplayer):
    assert 'http://foo.com/x' == dummy_videoplayer.props.src
